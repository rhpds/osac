# Module 04 — Bare Metal as a Service (BMaaS)

### Brief Overview

SAI Corp needs a dedicated server for a workload that must control its own operating system and hardware. Participants act as Sovereign Cloud Corp's platform administrator to register separate BMaaS capacity, define a hardware profile that does not compete with CaaS inventory, and publish a `BareMetalInstanceCatalogItem` backed by the BMaaS provisioning template. They then switch to Alice, SAI Corp's tenant administrator, to order a `BareMetalInstance`, connect to it over SSH, and halt and restart it through the tenant API. BMaaS provisions an operating system directly onto a registered host: in this RHDP environment a libvirt VM on the bare-metal fabric (BMF) host simulates a physical server, Sushy exposes its Redfish management interface, and Metal3/Ironic inspects and provisions it. Unlike CaaS, the order creates no HyperShift hosted control plane and no worker node — Alice receives a standalone server running Red Hat Enterprise Linux CoreOS (RHCOS).

### Audience and Time

**Audience**: Platform administrators and platform engineers who offer self-service dedicated servers to tenants, plus the tenant administrators who consume them.

**Prerequisites for this module**: Module 01 (Tenant Onboarding and Identity Management) complete. This module uses the `sai-corp` tenant and Alice's tenant administrator role; without them the exercises fail. Module 03 (CaaS) is useful background but is not required — you do not need to order a CaaS cluster to complete this module.

**Duration**: 30 min

### Learning Objectives

- Register a separate `BareMetalHost` and wait for Metal3 to make it available
- Define a hardware profile that selects BMaaS capacity without claiming CaaS hosts
- Publish a `BareMetalInstanceCatalogItem` backed by the BMaaS provisioning template
- Order a `BareMetalInstance` as a tenant administrator and connect with an SSH key
- Halt and restart the instance through the tenant API
- Release an instance and verify that its host returns to the available inventory

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Check the environment | 4 min |
| 2 | Register BMaaS capacity | 8 min |
| 3 | Publish the BMaaS offering | 4 min |
| 4 | Order and access a dedicated server | 9 min |
| 5 | Manage the instance lifecycle | 5 min |
| 6 | Release the server (optional) | — |

### Detailed Steps

1. Check the environment (platform administrator):
   - Log in to the OSAC fulfillment internal API with `osac login --private` using a dedicated `$HOME/admin` config directory, so the administrator and Alice sessions can coexist.
   - Confirm the BMaaS provisioning template `osac.templates.bm_host_provisioning` appears in `osac get baremetalinstancetemplates`.
   - Check that Sushy answers on `http://10.10.10.2:8000/redfish/v1/Systems` and that the `provisioning-configuration` resource has `watchAllNamespaces=true`.
   - List the current `BareMetalHost` inventory in the `osac` namespace and note how this module's capacity (`virtual-bmh-2`, MAC `52:54:00:ca:aa:02`, label `osac.openshift.io/host-type: bmaas`, instance type `c1-bmaas-amd64`) differs from Module 3's CaaS host.
2. Register BMaaS capacity (platform administrator):
   - Connect to the BMF host at `10.10.10.2` and list libvirt domains with `virsh list --all`.
   - If absent, create `virtual-bmh-2` with `virt-install` — 8192 MB memory, 4 vCPUs, a blank 60 GB qcow2 disk, MAC `52:54:00:ca:aa:02`, and the explicit `OVMF_CODE.fd` loader so Secure Boot firmware is not selected.
   - Verify the firmware, MAC, and UUID with `virsh dumpxml`, `domiflist`, and `domuuid`.
   - Back on the bastion, apply the BMC credential `Secret` and a `BareMetalHost` labeled `osac.openshift.io/host-type: bmaas`, with `bootMode: UEFI`, `automatedCleaningMode: disabled`, `rootDeviceHints.deviceName: /dev/vda`, and a `redfish-virtualmedia+http://10.10.10.2:8000/redfish/v1/Systems/${VM_UUID}` BMC address.
   - Watch the host move through `inspecting` -> `preparing` -> `available`, then confirm it is `OK` with no `consumerRef` — the inventory controller claims it when Alice orders.
3. Publish the BMaaS offering (platform administrator):
   - Create the `BareMetalInstanceType` `c1-bmaas-amd64` (4 cores, amd64, 1 thread per core, 8 GB memory, `enp1s0:fabric:Ethernet:10Gbps`) with `--host-label osac.openshift.io/host-type=bmaas` so it selects only BMaaS capacity.
   - Check the shared `DiskImage` `rhcos-4-22` and confirm its lifecycle is `DISK_IMAGE_LIFECYCLE_AVAILABLE`; create it from `oci://quay.io/osac-project/rhcos:4.22.0` only if the lab did not supply it.
   - Publish the `BareMetalInstanceCatalogItem` `demo-bm-default` against `--template osac.templates.bm_host_provisioning` with `--published`.
   - Validate the catalog item shows `published: true` and the expected template reference.
4. Order and access a dedicated server (Alice, tenant administrator):
   - Verify Alice's session with `osac whoami` (tenant `sai-corp`, role `tenant-admin`); re-login with the device flow and `--scopes=organization:sai-corp` if it expired.
   - Confirm `demo-bm-default` is visible from the tenant API and check whether `sai-corp-bm-1` already exists.
   - Generate an `ed25519` SSH key if needed and register the public key as an `ssh-public-key` `Secret` named `bmaas-ssh-key` in Alice's tenant.
   - Build an Ignition 3.4.0 document that adds the key to the RHCOS `core` account, since Metal3 metadata alone does not configure that account.
   - Place the order with `osac create baremetalinstance --name sai-corp-bm-1 --catalog-item demo-bm-default --disk-image rhcos-4-22 --set instance_type.name=c1-bmaas-amd64 --set instance_type.shared=true --ssh-key ... --user-data ... --run-strategy Always`.
   - Track the tenant instance (`PROVISIONING` -> `RUNNING`) and the `BareMetalHost` (`available` -> `provisioning` -> `provisioned`), allowing up to 10 minutes; do not interfere with the VM using `virsh destroy`.
   - As the administrator, map Alice's instance ID to the hub `BareMetalInstance` via the `osac.openshift.io/baremetalinstance-uuid` label and confirm `spec.externalHostID: osac/virtual-bmh-2`.
   - Read the boot NIC's IPv4 address from the BMH hardware inventory and SSH to `core@` that address through a `ProxyCommand` via the BMF host, confirming the guest reports Red Hat Enterprise Linux CoreOS.
5. Manage the instance lifecycle (Alice, tenant administrator):
   - Edit the instance with `osac edit baremetalinstance sai-corp-bm-1` and set `spec.run_strategy` to `BARE_METAL_INSTANCE_RUN_STRATEGY_HALTED`.
   - Confirm the instance reports `BARE_METAL_INSTANCE_STATE_STOPPED` and the BMH reports `online=false poweredOn=false`, while remaining `provisioned` and allocated.
   - Edit again to `BARE_METAL_INSTANCE_RUN_STRATEGY_ALWAYS` and repeat the checks until the instance is `RUNNING` with `online=true poweredOn=true`.
   - Re-run the SSH command to confirm the guest is reachable again.

### Learning Outcomes Checkpoint

Participants should have:

- Logged in to the OSAC fulfillment internal API as the platform administrator through a separate config directory
- Confirmed the `osac.templates.bm_host_provisioning` template, the Sushy Redfish endpoint, and Metal3's all-namespaces watch
- Distinguished this module's BMaaS capacity from Module 3's CaaS host by VM name, MAC, host-type label, and instance type
- Created the `virtual-bmh-2` libvirt VM on the BMF host with a blank disk and UEFI firmware without Secure Boot
- Applied a BMC `Secret` and a `BareMetalHost` labeled `osac.openshift.io/host-type: bmaas` pointing at the Sushy Redfish endpoint
- Waited for Metal3/Ironic to inspect the host and move it to `available` with no consumer
- Created the `c1-bmaas-amd64` `BareMetalInstanceType` with a `host-type=bmaas` selector
- Validated the `rhcos-4-22` `DiskImage` and published the `demo-bm-default` `BareMetalInstanceCatalogItem`
- Registered an `ssh-public-key` `Secret` and an Ignition user-data document in Alice's tenant
- Ordered `sai-corp-bm-1` as Alice and watched the host reach `provisioned` and the instance `RUNNING`
- Traced the tenant instance to the hub record and the claimed `BareMetalHost`
- Connected over SSH as `core` through the BMF host and confirmed RHCOS
- Halted and restarted the instance through `spec.run_strategy` and observed the matching BMH power state

### Key Takeaways

- BMaaS provisions an operating system directly onto a registered host; the tenant gets a standalone RHCOS server, not a hosted control plane or a cluster worker node.
- A `BareMetalHost` represents inventory; a `BareMetalInstance` represents a tenant's allocation of that inventory.
- Host-type labels and matching instance-type selectors let BMaaS and CaaS coexist on one platform without competing for the same hosts.
- Catalog items decouple ordering from implementation: the tenant picks an offering, disk image, and hardware profile, while the platform owns the provisioning template and the inventory behind it.
- Tenants never need BMC credentials or libvirt access — all lifecycle control flows through the tenant API.
- Halting retains the allocation and the disk; deleting the instance releases the host back to inventory.
- RHCOS guest access comes from Ignition user data, not from the SSH key recorded in Metal3 metadata.

### Infrastructure Notes

- The BMF host (`10.10.10.2`) runs libvirt and Sushy and is already set up in the RHDP lab; `virtual-bmh-2` is a libvirt VM reached through that host, and the worked example shows it at `192.168.122.208`.
- The explicit `OVMF_CODE.fd` loader is required in this lab — the generic `--boot uefi` option can select Secure Boot firmware and stop the inspection agent from booting.
- `automatedCleaningMode: disabled` is a lab convenience that skips an IPA cleaning cycle; a production service needs a real cleaning policy before reassigning hardware between tenants.
- Inspection and provisioning take several minutes each (allow up to 10 minutes for the order; the Solve button can take 10–30 minutes), and the OSAC list can leave `INTERNAL IP` empty on this simulated network, so the guest address comes from BMH hardware inventory or a libvirt DHCP lease.
- The module includes Solve and Validate buttons; validation expects a running server and must run before the optional Exercise 6 release step, which deletes the instance and returns the host to inventory (`-e bmaas_expected_state=released` checks the released state instead).
- If `virtual-bmh-2` already exists with another workload's consumer, separate capacity is needed — the content warns against relabeling or deleting an occupied host.
