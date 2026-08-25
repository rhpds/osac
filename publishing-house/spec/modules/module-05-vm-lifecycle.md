# Module 05 — Virtual Machine Lifecycle

### Brief Overview

This capstone module brings together all prior work: participants provision a virtual machine using the template from Module 3 and the network from Module 4, within the tenant created in Module 2. After managing basic VM lifecycle operations as an admin, participants switch to the end-user account to experience how a tenant user requests and accesses a VM — completing the full admin-to-user operational workflow.

### Audience and Time

**Audience**: OCX administrators and platform engineers; end-user perspective demonstrated for participants taking on both roles.

**Prerequisites for this module**: Modules 01–04 complete; a tenant, published template, and virtual network are all in place.

**Duration**: 30 min

### Learning Objectives

- Provision a virtual machine within an OCX tenant using a published template and virtual network
- Manage VM lifecycle operations including start, stop, and restart from the admin console
- Demonstrate the end-user perspective by requesting and accessing a VM as a tenant user
- Analyze the full OCX operational workflow from tenant creation through VM access

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Provision a VM as admin | 10 min |
| 2 | Manage VM lifecycle operations | 8 min |
| 3 | Switch to end-user perspective | 12 min |

### Detailed Steps

1. In the admin console, navigate to Virtual Machines and initiate VM creation, selecting the template created in Module 3.
2. Select the virtual network and subnetwork from Module 4, and review any additional VM properties before provisioning.
3. Start the VM and monitor its progress until it reaches a running state; confirm it is accessible.
4. Perform lifecycle operations from the admin console: stop the VM, restart it, and observe state transitions.
5. Log in to the end-user account and navigate to the self-service interface to request a VM within the assigned tenant.
6. Access the provisioned VM as an end user and verify the experience from the consumer perspective.

### Key Takeaways

- VM provisioning in OCX integrates templates, networks, and tenant context into a single, repeatable workflow.
- The platform manages the complete VM lifecycle — creation, start, stop, restart, and deletion — through a unified interface.
- End users interact with a simplified self-service interface, consuming admin-configured resources without exposure to platform internals.
- Understanding both the admin and end-user perspectives is essential to operating OCX effectively in a production environment.

### Infrastructure Notes

- VM provisioning time depends on the base image size; the lab environment is tuned to minimize wait time.
- The end-user account must be assigned to the tenant (completed in Module 2) for the end-user perspective section to work.
- Assessment is observation-based: participants demonstrate the expected state in the OCX UI or via CLI output.
