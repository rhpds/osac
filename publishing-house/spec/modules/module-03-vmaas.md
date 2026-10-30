# Module 03 — Virtual Machine as a Service (VMaaS)

### Brief Overview

SAI Corp's tenant is onboarded, users are federated, and role-based access control is enforced. Participants close the compute gap by configuring storage, disk images, instance types, and catalog items as the Sovereign Cloud Corp platform administrator. Alice, the SAI Corp tenant administrator, deploys a virtual machine from the catalog, and participants verify that Bob, the project viewer, can see the VM but cannot create or delete one.

### Audience and Time

**Audience**: Platform administrators who build self-service VM provisioning for tenants with Red Hat cloud extensions.

**Prerequisites for this module**: Module 02 complete — the `sai-corp` tenant and users Alice and Bob must exist. Participants who skipped Module 02 can click its *Solve* button.

**Duration**: 30 min

### Learning Objectives

- Configure a storage backend and storage tier for tenant workloads
- Create disk images and instance types as platform-level building blocks
- Author and publish a `ComputeInstanceCatalogItem` referencing a VM template
- Deploy a virtual machine from the catalog as a tenant administrator
- Verify that RBAC enforcement prevents unauthorized VM operations

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Configure storage for tenant workloads | 5 min |
| 2 | Publish VM building blocks to the catalog | 6 min |
| 3 | Verify tenant networking | 3 min |
| 4 | Deploy a virtual machine | 12 min |
| 5 | Verify tenant user access | 4 min |

### Detailed Steps

1. Configure storage for tenant workloads:
   - As the platform administrator, create a storage backend named `local` using the LVMS provider and capture its UUID.
   - Create the `local` storage tier with `--protocol BLOCK`.
   - Label the `lvms-vg1` storage class for the `sai-corp` tenant and `local` storage tier.
   - Verify the tenant shows `Ready` with a `local` storage class, and optionally confirm the tier under *Infrastructure → Storage Tiers* in the UI.
2. Publish VM building blocks to the catalog:
   - Create a Fedora disk image from `quay.io/containerdisks/fedora:latest` and verify it reaches `AVAILABLE`.
   - Create the `small-1-2` instance type (1 vCPU, 2 GiB RAM) and verify it is `ACTIVE`.
   - Author `${HOME}/yaml/standard-linux-vm.yaml` as a `ComputeInstanceCatalogItem` referencing `osac.templates.ocp_virt_vm` with `published: true`.
   - Apply the catalog item and verify it shows `true` in the published column.
3. Verify tenant networking:
   - As Alice, verify the auto-provisioned `default` virtual network, `default-ipv4` subnet, and `default` security group are `READY`.
   - Capture the subnet and security group IDs for VM creation.
4. Deploy a virtual machine:
   - As Alice, retrieve the catalog item, subnet, and security group IDs, then create `portal-vm` with `osac create computeinstance` using the instance type, disk image, boot disk, network attachment, and cloud-init user data flags.
   - Work around the known disk import issue as cluster administrator by finding the VM namespace, VM name, and DataVolume name, halting the VM, deleting the stuck DataVolume, recreating it with `pullMethod: node`, waiting for `Succeeded`, and restarting the VM with `runStrategy: Always`.
   - Verify `portal-vm` reaches `RUNNING` with an IP address on the tenant subnet and confirm the KubeVirt `VirtualMachine` and `VirtualMachineInstance` are running.
   - Open the serial console, log in as `fedora-admin`, check `/etc/os-release`, and disconnect.
5. Verify tenant user access:
   - As Bob, confirm he has no `tenant-admin` role, list compute instances, and see Alice's VM.
   - Confirm Bob cannot delete `portal-vm` or create a new VM; both attempts must return `PermissionDenied`.

### Learning Outcomes Checkpoint

Participants should have:

- Configured a storage backend and storage tier for tenant workloads
- Labeled the Kubernetes storage class to map the `local` tier to the `sai-corp` tenant
- Created a Fedora disk image and a compute instance type as platform building blocks
- Authored and published a `ComputeInstanceCatalogItem` referencing the OpenShift Virtualization template
- Deployed a virtual machine from the catalog as tenant administrator Alice
- Verified the VM reached `RUNNING` state with an IP address on the tenant subnet
- Confirmed RBAC enforcement: Bob can view the VM but cannot create or delete one

### Key Takeaways

- Storage tiers bridge Kubernetes and the catalog: the `local` tier links a Kubernetes storage class to the fulfillment workflow.
- Catalog items are self-service templates: tenants specify parameters such as disk image, instance type, and networking at ordering time via CLI flags.
- RBAC extends to workloads: viewers can see compute instances but cannot create or destroy them.
- Platform administrators control storage, images, instance types, and catalog items; tenant administrators control what is deployed.

### Infrastructure Notes

- Red Hat cloud extensions auto-provisions a default virtual network, subnet, and security group for each tenant.
- CDI cannot pull the disk image from quay.io inside the pod network because the cluster has no external access. The module fixes this by recreating the DataVolume with `pullMethod: node` and the `lvms-vg1` storage class.
- The VM password comes from the `osac_user_password` attribute.
- The module Solve button configures storage for `sai-corp`, publishes the disk image, instance type, and `standard-linux-vm` catalog item, deploys `portal-vm` as Alice, and verifies Bob's viewer restrictions.
