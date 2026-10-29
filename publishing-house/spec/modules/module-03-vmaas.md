# Module 03 — Virtual Machine as a Service (VMaaS)

### Brief Overview

SAI Corp's tenant is onboarded, but its teams need virtual machines they can provision on demand. Acting as the Sovereign Cloud Corp platform administrator, participants configure storage, a disk image, an instance type, and a `ComputeInstanceCatalogItem` in Red Hat cloud extensions. Alice, the SAI Corp tenant administrator, then verifies tenant networking and deploys a VM from the catalog. Finally, participants confirm that Bob, a project viewer, can see the VM but cannot create or delete one.

### Audience and Time

**Audience**: Platform administrators who build self-service VM provisioning for tenants with Red Hat cloud extensions.

**Prerequisites for this module**: Module 02 complete — the `sai-corp` tenant and users Alice and Bob must exist. Participants who skipped Module 02 can click its *Solve* button.

**Duration**: 20 min

### Learning Objectives

- Configure a storage backend and storage tier for tenant workloads
- Create a disk image and an instance type as platform-level building blocks
- Publish a `ComputeInstanceCatalogItem` that references a VM template
- Deploy a virtual machine from the catalog as a tenant administrator
- Verify that RBAC prevents a project viewer from creating or deleting VMs

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Configure storage for tenant workloads | 3 min |
| 2 | Publish VM building blocks to the catalog | 4 min |
| 3 | Verify tenant networking | 2 min |
| 4 | Deploy a virtual machine | 8 min |
| 5 | Verify tenant user access | 3 min |

### Detailed Steps

1. As the platform administrator, create a storage backend named `local` with the LVMS provider (`osac create storagebackend`) and capture its UUID.
2. Create the `local` storage tier on that backend (`osac create storagetier --protocol BLOCK`).
3. Label the `lvms-vg1` storage class with the `sai-corp` tenant and the `local` storage tier (`oc label sc`).
4. Verify the `sai-corp` tenant shows `Ready` with a `local` tier storage class. Optionally confirm the tier in the UI under *Infrastructure → Storage Tiers*.
5. Create the `fedora` disk image from `quay.io/containerdisks/fedora:latest` (`osac create diskimage`) and verify it reaches `AVAILABLE`.
6. Create the `small-1-2` instance type (1 vCPU, 2 GiB RAM) with `osac create instancetype` and verify it is `ACTIVE`.
7. Write `standard-linux-vm.yaml`, a `ComputeInstanceCatalogItem` that references the `osac.templates.ocp_virt_vm` template with `published: true`, then apply it with `osac create -f`.
8. Verify the catalog item shows `true` in the published column (`osac get computeinstancecatalogitem`).
9. As Alice, verify that the auto-provisioned `default` virtual network, `default-ipv4` subnet, and `default` security group are `READY`, then save the subnet and security group IDs.
10. As Alice, retrieve the catalog item, subnet, and security group IDs, then create `portal-vm` with `osac create computeinstance`. Pass the instance type, disk image, boot disk, network attachment, and cloud-init user data as flags.
11. Work around the known disk import issue as cluster administrator. Find the VM namespace, VM name, and DataVolume name, halt the VM, delete the stuck DataVolume, and recreate it with `pullMethod: node`.
12. Watch the DataVolume until it reaches `Succeeded`, then restart the VM with `runStrategy: Always`.
13. Verify `portal-vm` is `RUNNING` with an IP address in the tenant subnet, and that the KubeVirt `VirtualMachine` and `VirtualMachineInstance` show `Running`.
14. Open the serial console (`osac console serial computeinstance portal-vm`), log in as `fedora-admin`, check `/etc/os-release`, and disconnect.
15. As Bob, run `osac whoami` to confirm he has no `tenant-admin` role, then list compute instances and see Alice's VM.
16. Confirm that Bob cannot delete `portal-vm` or create a new VM; both attempts return `PermissionDenied`.

### Key Takeaways

- Storage tiers connect Kubernetes storage classes to the fulfillment workflow. Without the `local` tier mapping, VM creation fails at the boot disk step.
- Catalog items are self-service templates that reference a VM template. Tenants specify disk image, instance type, and networking at ordering time with CLI flags.
- The RBAC model from Module 02 also governs compute instances: viewers can see workloads but cannot create or delete them.
- Platform administrators control what is available (storage, images, instance types, catalog items), and tenant administrators control what is deployed.

### Infrastructure Notes

- Red Hat cloud extensions auto-provisions a default virtual network, subnet, and security group for each tenant.
- CDI cannot pull the disk image from quay.io inside the pod network because the cluster has no external access. The module fixes this by recreating the DataVolume with `pullMethod: node` and the `lvms-vg1` storage class.
- The VM password comes from the `osac_user_password` attribute.
- The module *Solve* button configures storage, publishes the disk image, instance type, and catalog item, deploys `portal-vm` as Alice, and verifies Bob's viewer restrictions.
