# Module 04 — Cluster as a Service (CaaS)

### Brief Overview

SAI Corp can now provision virtual machines through the VMaaS catalog, but its platform engineers also need full OpenShift clusters for CI/CD pipelines, containerized workloads, and isolated test environments. Participants enable Cluster as a Service (CaaS) for the OSAC platform by validating the Sushy emulator, registering a `BareMetalHost`, publishing cluster catalog objects, and ordering a hosted OpenShift cluster as Alice. The platform orchestrates a HyperShift Hosted Control Plane whose worker node boots onto the registered bare-metal host.

### Audience and Time

**Audience**: Platform administrators and platform engineers who offer self-service OpenShift clusters to tenants.

**Prerequisites for this module**: Module 02 complete. This module uses the `sai-corp` tenant and the users Alice and Bob created there; without them the exercises fail.

**Duration**: 30 min

### Learning Objectives

- Validate the Sushy setup on the BMF host so Ironic can manage libvirt VMs through Redfish
- Register a `BareMetalHost` pointing at the Sushy/Redfish endpoint
- Wait for Metal3 to inspect and make the host available
- Publish platform catalog objects: `BareMetalInstanceType`, `DiskImage`, `ClusterVersion`, and `ClusterCatalogItem`
- Order a hosted OpenShift cluster as a tenant using the OSAC CLI

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Set up the lab environment | 3 min |
| 2 | Configure platform networking | 3 min |
| 3 | Provision a bare-metal worker host | 7 min |
| 4 | Publish cluster catalog objects | 4 min |
| 5 | Order a hosted cluster as a tenant administrator (Alice) | 8 min |
| 6 | Access the hosted cluster | 5 min |

### Detailed Steps

1. Set up the lab environment:
   - Verify the Sushy emulator responds on the BMF host.
   - Generate an SSH key pair if needed.
   - Extract the cluster pull secret from `openshift-config`.
   - Log in to the OSAC private API as the cloud administrator and confirm CaaS and BMaaS are enabled.
2. Configure platform networking:
   - Validate that the Metal3 operator watches `BareMetalHosts` in all namespaces.
   - Verify OSAC inventory is configured for Metal3 and the `osac` namespace.
   - Verify the fulfillment service uses the `noop` DNS driver for RHDP environments.
   - Verify the `k8s-only` NetworkClass has a fabric manager.
3. Provision a bare-metal worker host:
   - Connect to the BMF host, create a blank-disk `virtual-bmh-1` libvirt VM with UEFI Secure Boot off and a fixed MAC address, and confirm it is running.
   - Back on the bastion, create the BMC secret and `BareMetalHost` labeled `osac.openshift.io/host-type: default`.
   - Watch the host move through `registering` and `inspecting` to `available`.
   - Verify the Ironic-to-IPA return path through the BMF host.
4. Publish cluster catalog objects:
   - Create and validate a `BareMetalInstanceType`.
   - Validate the RHCOS `DiskImage` and available `ClusterVersions`.
   - Create, publish, and validate a `ClusterCatalogItem`.
5. Order a hosted cluster as Alice:
   - Confirm Alice's session and the published catalog item.
   - Create a pull secret in Alice's tenant and place the cluster order with `--catalog-item`.
   - Check that the cluster is `Progressing` and inspect the `ClusterOrder`.
   - Apply the `dns.noop` lab workarounds: verify the tenant default subnet, wait for the MetalLB API VIP, publish `api` and `api-int` in libvirt DNS, wait for Ironic provisioning, provide temporary wildcard DNS for the discovery agent, link the worker node to the hub machine record with `providerID`, point `*.apps` routes at the worker, and verify the cluster reaches `Ready`.
6. Access the hosted cluster:
   - Publish the hosted API through a hub `passthrough` route and test it.
   - Check hub-to-worker ingress reachability.
   - Publish the console on the hub, give the console and OAuth server a trusted certificate for the public hostname, and open the console in a browser.

### Learning Outcomes Checkpoint

Participants should have:

- Validated the Sushy Redfish emulator on the BMF host
- Patched Metal3 to watch BareMetalHosts in all namespaces and waited for its webhook
- Verified the fulfillment service uses the `noop` DNS driver for RHDP environments
- Verified the `k8s-only` NetworkClass has a fabric manager so bare-metal workers can be allocated
- Created a worker libvirt VM with UEFI Secure Boot off on the BMF host
- Applied a `BareMetalHost` and BMC secret pointing at the Sushy Redfish endpoint
- Waited for Metal3 / Ironic to inspect and move the BMH to `available`
- Verified the Ironic-to-IPA return path through the BMF host
- Created and validated `BareMetalInstanceType`, `DiskImage`, `ClusterVersion`, and `ClusterCatalogItem`
- Ordered a hosted OpenShift cluster as Alice, tenant admin for `sai-corp`
- Supplied the DNS, `providerID`, and ingress workarounds a `dns.noop` lab needs
- Verified the cluster reached a `Ready` worker node via the guest kubeconfig
- Published the hosted cluster API and console through the hub router and logged in as `kubeadmin`

### Key Takeaways

- HyperShift separates control plane from workers: the hosted control plane runs as pods on the hub cluster and the worker node is a bare-metal host, or a libvirt VM behind Sushy in this lab.
- Sushy emulates a Redfish BMC for each libvirt VM, so Ironic interacts with it exactly as it would a real iDRAC or iLO.
- BMaaS and CaaS are independently gated by Helm feature flags, but `BareMetalInstanceType` and cluster node provisioning require BMaaS.
- Catalog items decouple ordering from implementation: tenants specify `--catalog-item`, while the platform controls the template, OCP version, and hardware profile behind it.
- `--catalog-item` replaces the deprecated `--template` flag for cluster orders; the two flags are mutually exclusive.

### Infrastructure Notes

- The BMF host (`10.10.10.2`) runs libvirt and Sushy and is already set up in the RHDP lab.
- The worker is a libvirt VM on `192.168.122.0/24` behind the BMF host.
- The environment uses the `noop` DNS driver, so the DNS, `providerID`, ingress, and route-publishing workarounds are lab-specific.
- Worker provisioning and agent installation take several minutes each; the content includes troubleshooting and an appendix for non-RHDP BMF setup.
