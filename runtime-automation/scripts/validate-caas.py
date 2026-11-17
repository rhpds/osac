#!/usr/bin/env python3
"""Read-only end-state checks for the BMF/Metal3 CaaS lab."""

import base64
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ready(resource, condition):
    return any(item.get("type") == condition and item.get("status") == "True"
               for item in resource.get("status", {}).get("conditions", []))


def validate_snapshot(snapshot):
    order, bmh, bmi, hc = (snapshot[key] for key in ("order", "bmh", "bmi", "hc"))
    name = order["metadata"]["name"]
    require(order.get("status", {}).get("phase") == "Ready", "ClusterOrder is not Ready")
    require(bmh["metadata"].get("namespace") == "osac"
            and bmh["metadata"]["name"] == "virtual-bmh-1", "Wrong lab BareMetalHost")
    require(bmh.get("spec", {}).get("online") is True, "BareMetalHost is offline")
    require(bmh.get("status", {}).get("provisioning", {}).get("state") == "provisioned",
            "BareMetalHost has not completed provisioning")
    require(not bmh.get("status", {}).get("errorMessage"), "BareMetalHost reports an error")
    consumer = bmh.get("spec", {}).get("consumerRef", {})
    require(consumer.get("name") == bmi["metadata"]["name"]
            and consumer.get("uid") == bmi["metadata"].get("uid")
            and bool(consumer.get("uid")), "BareMetalInstance is not the host's consumer")
    require(bmi.get("status", {}).get("phase") == "Ready", "BareMetalInstance is not Ready")
    require(hc["metadata"]["name"] == name
            and hc["metadata"]["namespace"] == "osac-" + name,
            "HostedCluster does not match the selected order")
    require(ready(hc, "Available"), "HostedCluster is not Available")
    pools = [pool for pool in snapshot["nodepools"] if pool.get("spec", {}).get("clusterName") == name]
    require(len(pools) == 1 and pools[0]["spec"].get("replicas") == 1
            and pools[0].get("status", {}).get("readyReplicas") == 1,
            "Expected one Ready worker replica in the order's NodePool")
    addresses = {nic.get("ip") for nic in bmh.get("status", {}).get("hardware", {}).get("nics", [])}
    addresses.discard(None)
    workers = [node for node in snapshot["nodes"]
               if "node-role.kubernetes.io/worker" in node.get("metadata", {}).get("labels", {})
               and ready(node, "Ready")
               and any(address.get("type") == "InternalIP" and address.get("address") in addresses
                       for address in node.get("status", {}).get("addresses", []))]
    require(len(workers) == 1, "No unique Ready worker matches the provisioned host IP")


def command(argv):
    result = subprocess.run(argv, capture_output=True, text=True, timeout=90)
    if result.returncode:
        # Never echo kubeconfig contents or credential-bearing command output.
        raise ValueError("Read-only command failed: " + argv[0])
    return result.stdout


def get(kind, name=None, namespace=None, oc_args=None):
    argv = ["oc", *(oc_args or []), "get", kind]
    if name:
        argv.append(name)
    if namespace:
        argv.extend(["-n", namespace])
    return json.loads(command([*argv, "-o", "json"]))


def main():
    orders = get("clusterorders", namespace="osac")["items"]
    requested = os.environ.get("CAAS_ORDER_NAME", "")
    selected = [order for order in orders if not requested or order["metadata"]["name"] == requested]
    require(len(selected) == 1, "Select exactly one lab order with CAAS_ORDER_NAME; never use newest implicitly")
    order = selected[0]
    name = order["metadata"]["name"]
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]*", name)), "Invalid order name")
    namespace = "osac-" + name
    bmh = get("baremetalhost", "virtual-bmh-1", "osac")
    consumer = bmh.get("spec", {}).get("consumerRef", {})
    require(consumer.get("namespace") == "osac" and bool(consumer.get("name")),
            "Host has no OSAC consumer; provisioning is incomplete")
    bmi = get("baremetalinstance", consumer["name"], "osac")
    hc = get("hostedcluster", name, namespace)
    pools = get("nodepools", namespace=namespace)["items"]
    secret = get("secret", name + "-admin-kubeconfig", namespace)
    vip = get("service", "kube-apiserver", namespace + "-" + name)["status"]["loadBalancer"]["ingress"][0]["ip"]
    ipaddress.ip_address(vip)
    # Private credentials exist only for the duration of these read-only checks.
    with tempfile.TemporaryDirectory(prefix="caas-validation-") as directory:
        path = Path(directory) / "kubeconfig"
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(base64.b64decode(secret["data"]["kubeconfig"], validate=True))
        # The documented lab uses this internal VIP and its cluster-local certificate.
        nodes = get("nodes", oc_args=["--kubeconfig", str(path),
                    "--server", f"https://{vip}:6443", "--insecure-skip-tls-verify"])["items"]
    validate_snapshot({"order": order, "bmh": bmh, "bmi": bmi, "hc": hc,
                       "nodepools": pools, "nodes": nodes})
    domain = get("ingress.config.openshift.io", "cluster")["spec"]["domain"]
    require(bool(re.fullmatch(r"[A-Za-z0-9.-]+", domain)), "Invalid ingress domain")
    console = f"https://console-{name}.{domain}/"
    with urllib.request.urlopen(console, timeout=30) as response:
        require(response.status == 200, "Published console did not return HTTP 200 over trusted TLS")
    print(json.dumps({"status": "pass", "scope": "module-04-current-topology-end-state",
                      "order": name, "baremetal_host": "virtual-bmh-1",
                      "hosted_cluster_available": True, "matching_worker_ready": True,
                      "console_tls_verified": True}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, IndexError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "fail", "scope": "module-04-current-topology-end-state",
                          "error": str(error)}))
        raise SystemExit(1)
