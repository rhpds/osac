# Module 03 — VM Templates

### Brief Overview

VM templates define the standard configuration from which virtual machines are provisioned. This module covers building a template from an available base image, configuring its compute resource defaults, and publishing it to the tenant created in Module 2. After completing this module, the tenant has a ready-to-use template that Module 5 will consume when provisioning VMs.

### Audience and Time

**Audience**: OSAC administrators responsible for defining and publishing standardized VM configurations for tenant use.

**Prerequisites for this module**: Module 02 complete; a tenant exists in the environment.

**Duration**: 15 min

### Learning Objectives

- Build a VM template from an available base image within the OSAC admin console
- Configure template compute resource parameters (CPU, memory, disk)
- Publish the template to an OSAC tenant so it is available for VM provisioning

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Review available base images | 4 min |
| 2 | Create and configure a VM template | 7 min |
| 3 | Publish the template to the tenant | 4 min |

### Detailed Steps

1. Navigate to the VM Templates section of the OSAC admin console and review the available base images.
2. Initiate template creation by selecting an appropriate base image.
3. Configure the template properties: name, description, CPU count, memory allocation, and disk size.
4. Assign the template to the tenant created in Module 2.
5. Confirm the template is visible and in a published state within the tenant context.

### Key Takeaways

- VM templates standardize how virtual machines are configured and deployed across tenants.
- Templates are created at the admin level using pre-approved base images, ensuring consistent and controlled VM configurations.
- Publishing a template to a tenant makes it available for end users to consume without exposing underlying platform configuration.
- Template resource parameters define default allocations; quotas set in Module 2 govern the ceiling.

### Infrastructure Notes

- Base images are pre-loaded in the lab environment — no image upload is required.
- The template created in this module is referenced in Module 5 when provisioning a VM.
