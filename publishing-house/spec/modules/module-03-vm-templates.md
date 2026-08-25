# Module 03 — OCX Compute Catalog

### Brief Overview

Before tenants can provision VMs, the platform admin must publish what's available to order. OCX splits this into two concepts: **InstanceTypes** (named VM size bundles — like cloud instance flavors) and **ComputeInstanceCatalogItems** (published products tenants select from a service catalog when creating a VM). This module covers creating both, making them available to tenants, and verifying they appear correctly in the tenant VM creation wizard.

### Audience and Time

**Audience**: OCX administrators responsible for defining and publishing the VM catalog for tenant use.

**Prerequisites for this module**: Module 02 complete; a tenant exists in the environment.

**Duration**: 20 min

### Learning Objectives

- Create an InstanceType that defines an approved VM size available to tenants
- Publish a ComputeInstanceCatalogItem that specifies the VM image, boot disk, and configurable fields for tenant ordering
- Verify that both the instance type and catalog item appear in the tenant VM creation wizard

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Create an InstanceType | 5 min |
| 2 | Publish a Catalog Item | 10 min |
| 3 | Verify in the tenant VM wizard | 5 min |

### Detailed Steps

1. Create an InstanceType using the OCX private API or CLI:
   ```bash
   osac create -f demo-small-1-2.yaml
   # "@type": type.googleapis.com/osac.private.v1.InstanceType
   # spec: cores: 1, memory_gib: 2
   osac get instancetype    # verify STATE = ACTIVE
   ```
2. Observe that InstanceTypes are **immutable after creation** — `cores` and `memory_gib` cannot be changed. States flow ACTIVE → DEPRECATED → OBSOLETE; tenants see ACTIVE and DEPRECATED types.
3. Create a ComputeInstanceCatalogItem using `osac create -f`:
   ```bash
   osac create -f demo-linux-vm.yaml
   # "@type": type.googleapis.com/osac.private.v1.ComputeInstanceCatalogItem
   # template: osac.templates.ocp_virt_vm
   # published: true
   # field_definitions: ssh_key, image.source_ref, boot_disk.size_gib, instance_type, network_attachments
   ```
4. Confirm the catalog item is published: `osac get computeinstancecatalogitem demo-linux-vm`.
5. Review the `field_definitions` — these control exactly what tenants can customize when ordering a VM. Fields not in `field_definitions` cannot be set by the tenant.
6. Log in to the tenant account and open the VM creation wizard in the OCX UI.
7. Confirm **Demo Linux VM** appears in the catalog, and **demo-small-1-2 — 1 vCPU, 2 GiB** appears in the Instance Type dropdown.

### Key Takeaways

- OCX separates VM sizing (InstanceType) from VM definition (Catalog Item) — admins publish both; tenants combine them when ordering.
- A **Catalog Item** (`ComputeInstanceCatalogItem`) is a published service catalog entry: it references a provisioning template, sets image defaults, and controls which fields tenants can customize via `field_definitions`.
- `field_definitions` must include `instance_type` and `network_attachments` for the tenant VM wizard to function correctly — omitting them causes wizard errors.
- Setting `published: true` is required for the catalog item to appear to tenants; unpublished items are invisible in the tenant catalog.

### Infrastructure Notes

- InstanceTypes are stored in the fulfillment service database — there is no Kubernetes CR and no AAP provisioning step. Create is immediate.
- The catalog item template `osac.templates.ocp_virt_vm` is pre-deployed in the lab environment.
- Base images referenced in the catalog item (`quay.io/containerdisks/fedora:latest`) are pulled at VM creation time, not at catalog item creation.
- The catalog item created in this module is used in Module 5 when participants provision a VM.
