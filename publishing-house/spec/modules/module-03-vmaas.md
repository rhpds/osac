# Module 03 — Virtual Machine as a Service (VMaaS)

### Brief Overview

SAI Corp's tenant is onboarded, users are federated, and role-based access control is enforced. Participants close the compute gap by reviewing the platform-provisioned storage and creating disk images, instance types, and catalog items as the Sovereign Cloud Corp platform administrator. Alice, the SAI Corp tenant administrator, deploys a virtual machine from the catalog, and participants verify the boundary between the tenant and the platform: Bob can see the VM in his project but cannot publish catalog items or define instance types.

### Audience and Time

**Audience**: Platform administrators who build self-service VM provisioning for tenants with Red Hat cloud extensions.

**Prerequisites for this module**: Module 02 complete — the `sai-corp` tenant and users Alice and Bob must exist. Participants who skipped Module 02 can click its *Solve* button.

**Duration**: 30 min

### Learning Objectives

- Identify the storage backend, storage tier, and per-tenant storage classes that the platform provisions
- Create disk images and instance types as platform-level building blocks
- Author and publish a `ComputeInstanceCatalogItem` referencing a VM template
- Deploy a virtual machine from the catalog as a tenant administrator
- Verify that tenant users can consume the catalog but cannot change what the platform offers

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Review the platform storage configuration | 3 min |
| 2 | Publish VM building blocks to the catalog | 6 min |
| 3 | Verify tenant networking | 3 min |
| 4 | Deploy a virtual machine | 12 min |
| 5 | Verify the platform and tenant boundary | 4 min |

### Detailed Steps

1. Review the platform storage configuration (read-only — the platform provisions all of it):
   - Run `oc get sc` and identify the three `osac-<tenant>-<tier>` storage classes: `osac-shared-local` and `osac-system-local` from the platform deployment, and `osac-sai-corp-local` created automatically with the tenant in Module 2.
   - As the platform administrator, run `osac get storagebackend` to show the single LVMS backend named `local`.
   - Run `osac get storagetier` to show the `local` tier (`BLOCK`, `ACTIVE`) — the name Alice passes to `--boot-disk-storage-tier` in section 4.
   - Optionally confirm the tier under *Infrastructure → Storage Tiers* in the UI.
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
5. Verify the platform and tenant boundary:
   - As Bob, confirm he has no `tenant-admin` role, list compute instances, and see Alice's VM in the project his membership covers.
   - Confirm Bob cannot administer the tenant: `osac get users` returns `PermissionDenied`.
   - Confirm Bob cannot change what the platform offers: creating a `ComputeInstanceCatalogItem` and creating an instance type both return `PermissionDenied`.
   - Do not have Bob attempt to delete or create a compute instance. His project membership grants him authority over workloads in his own project, so those attempts succeed and destroy state module 4 depends on.

### Learning Outcomes Checkpoint

Participants should have:

- Reviewed the platform storage: the `local` backend and tier, and the `osac-sai-corp-local` storage class the platform created with the tenant
- Created a Fedora disk image and a compute instance type as platform building blocks
- Authored and published a `ComputeInstanceCatalogItem` referencing the OpenShift Virtualization template
- Deployed a virtual machine from the catalog as tenant administrator Alice
- Verified the VM reached `RUNNING` state with an IP address on the tenant subnet
- Confirmed the platform boundary: Bob can see the VM in his project but cannot publish a catalog item or define an instance type

### Key Takeaways

- Storage tiers bridge Kubernetes and the catalog: the `local` tier links a Kubernetes storage class to the fulfillment workflow. The platform provisions the backend, the tier, and a per-tenant `osac-<tenant>-local` storage class.
- Catalog items are self-service templates: tenants specify parameters such as disk image, instance type, and networking at ordering time via CLI flags.
- RBAC extends to workloads: a project member sees and works with the compute instances in their project; tenant-level and platform-level operations stay out of reach.
- Platform administrators control storage, images, instance types, and catalog items; tenant administrators control what is deployed.

### Infrastructure Notes

- Red Hat cloud extensions provisions the LVMS storage backend `local` and the `local` storage tier at platform deployment, and creates one `osac-<tenant>-<tier>` storage class per tenant. No manual storage setup or storage class labeling is needed.
- Red Hat cloud extensions auto-provisions a default virtual network, subnet, and security group for each tenant.
- CDI cannot pull the disk image from quay.io inside the pod network because the cluster has no external access. The module fixes this by recreating the DataVolume with `pullMethod: node` and the `lvms-vg1` storage class.
- The VM password comes from the `osac_user_password` attribute.
- The module Solve button publishes the disk image, instance type, and `standard-linux-vm` catalog item, and deploys `portal-vm` as Alice. It does not run the Exercise 5 denial checks — those are negative tests and belong in validate.
