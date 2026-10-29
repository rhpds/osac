# Module 04 — Cluster as a Service (CaaS)

### Brief Overview

This module enables Cluster as a Service (CaaS) on the Red Hat cloud extensions platform. As the Sovereign Cloud Corp platform administrator, the learner validates the pre-configured Sushy Redfish emulator on the bare-metal fabric (BMF) host, registers a libvirt VM as a `BareMetalHost`, and publishes the catalog objects tenants need. Then, as Alice (SAI Corp tenant administrator), the learner orders a hosted OpenShift cluster with the `osac` CLI. HyperShift runs the control plane on the hub, and the worker node boots onto the registered bare-metal host. The learner finishes by publishing the hosted cluster's API and console through the hub router.

### Audience and Time

**Audience**: Platform administrators and platform engineers who offer self-service OpenShift clusters to tenants.

**Prerequisites for this module**: Module 02 complete. This module uses the `sai-corp` tenant users Alice and Bob created there; without them the exercises fail.

**Duration**: 25 min

### Learning Objectives

- Validate the Sushy setup on the BMF host so Ironic can manage libvirt VMs through Redfish
- Register a `BareMetalHost` that points at the Sushy Redfish endpoint
- Verify that Metal3 inspects the host and makes it `available`
- Publish the platform catalog objects: `BareMetalInstanceType`, `DiskImage`, `ClusterVersion`, and `ClusterCatalogItem`
- Order a hosted OpenShift cluster as a tenant using the `osac` CLI
- Access the hosted cluster's API and console through the hub router

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Set up the lab environment | 3 min |
| 2 | Configure platform networking | 3 min |
| 3 | Provision a bare-metal worker host | 6 min |
| 4 | Publish cluster catalog objects | 4 min |
| 5 | Order a hosted cluster as the tenant administrator (Alice) | 6 min |
| 6 | Access the hosted cluster | 3 min |

### Detailed Steps

1. Set up the lab environment: verify the Sushy emulator responds on the BMF host, generate an SSH key pair if needed, extract the cluster pull secret from `openshift-config`, log in to the OSAC private API as the cloud administrator, and confirm that CaaS and BMaaS are both enabled.
2. Configure platform networking: validate that the Metal3 operator watches `BareMetalHosts` in all namespaces, verify that OSAC inventory is configured for the `osac` namespace, verify that the fulfillment service uses the `noop` DNS driver, and verify the `k8s-only` NetworkClass fabric manager.
3. Provision a bare-metal worker host: on the BMF host, create a blank-disk worker VM with a fixed MAC address, confirm Secure Boot is off, and check that the VM is running. Back on the bastion, create the BMC secret and the `BareMetalHost` labeled `osac.openshift.io/host-type: default`, watch it move through `registering` → `inspecting` → `available`, and verify the Ironic-to-IPA return path (MachineConfig on the hub).
4. Publish cluster catalog objects: create and validate a `BareMetalInstanceType`, validate the RHCOS `DiskImage` and the available `ClusterVersions`, then create, publish, and validate a `ClusterCatalogItem`.
5. Order a hosted cluster as Alice: confirm the Alice session and the published catalog item, create a pull secret in Alice's tenant, and place the cluster order with `--catalog-item`. Check that the cluster is `Progressing` and inspect the `ClusterOrder`. Apply the `dns.noop` lab workarounds: check that the tenant's default subnet is `Ready`, wait for the MetalLB API VIP and publish `api` and `api-int` in libvirt DNS, wait for Ironic to provision the worker, give the discovery agent temporary wildcard DNS, and wait for the agent to join the hosted cluster. Connect to the hosted cluster, link the worker node to the hub's machine record (`providerID`), point the `*.apps` routes at the worker, and verify that the cluster reaches `Ready` from the platform side, on the hub, and from inside the cluster.
6. Access the hosted cluster: publish the hosted API through a hub `passthrough` route and test it, check hub-to-worker ingress reachability, publish the console on the hub, give the console and OAuth server a trusted certificate for the public hostname, and open the console in a browser.

### Key Takeaways

- HyperShift separates the control plane from the workers: the hosted control plane runs as pods on the hub, and the worker runs on a bare-metal host.
- Sushy emulates a Redfish BMC for libvirt VMs, so Ironic manages them exactly as it would a physical server with iDRAC or iLO.
- BMaaS and CaaS are gated independently by Helm feature flags, but `BareMetalInstanceType` and cluster node provisioning require BMaaS.
- Catalog items decouple ordering from implementation: tenants pick a `--catalog-item`, and the platform controls the template, OCP version, and hardware profile behind it.
- `--catalog-item` replaces the deprecated `--template` flag for cluster orders; the two flags are mutually exclusive.

### Infrastructure Notes

- Requires a BMF host running libvirt and the Sushy emulator; the module's appendix documents how to set this up outside RHDP, where it is already provisioned.
- The worker is a libvirt VM on `192.168.122.0/24` behind the BMF host; lab provisioning maintains the Ironic-to-IPA path, hub routes, and firewall rules.
- The environment uses the `noop` DNS driver (no external Route53 access), so the DNS, `providerID`, ingress, and route-publishing workarounds in Exercises 5 and 6 are lab-specific and not needed with a real DNS driver.
- Worker provisioning and agent installation take several minutes each; the page includes troubleshooting for stuck inspection, provisioning, and console availability.
