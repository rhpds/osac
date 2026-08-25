# Module 02 — Tenant Administration

### Brief Overview

Tenants are the primary organizational unit of OCX. This module walks participants through creating and configuring a tenant using the OCX admin interface. Participants define resource quotas, configure access policies, and assign users — giving them the foundation that all subsequent modules (templates, networks, VMs) are built upon.

### Audience and Time

**Audience**: OCX administrators and platform engineers responsible for setting up and operating multi-tenant environments.

**Prerequisites for this module**: Module 01 complete; admin console accessible.

**Duration**: 25 min

### Learning Objectives

- Create a new OCX tenant using the administrative interface
- Configure tenant properties including resource quotas
- Manage tenant user assignments and role bindings to separate admin and user responsibilities
- Verify that a newly created tenant is correctly reflected in the platform

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Create a new tenant | 10 min |
| 2 | Configure tenant quotas and settings | 9 min |
| 3 | Assign users and verify tenant state | 6 min |

### Detailed Steps

1. In the admin console, navigate to the Tenants section and initiate creation of a new tenant.
2. Provide the required tenant properties: name, description, and any required metadata fields.
3. Configure resource quotas that govern how much compute (CPU, memory, storage) the tenant may consume.
4. Assign the end-user account to the tenant with an appropriate role binding.
5. Review the completed tenant record and confirm it appears correctly in the tenant list.

### Key Takeaways

- Tenants are the central organizational boundary in OCX, scoping all resources (templates, networks, VMs) to an isolated unit.
- Resource quotas are defined at tenant creation and control the ceiling for all workloads within that tenant.
- Role-based access control separates administrative operations from end-user consumption.
- A correctly configured tenant is a prerequisite for publishing templates, creating networks, and provisioning VMs.

### Infrastructure Notes

- The tenant created in this module is used throughout Modules 3, 4, and 5 — participants should use consistent naming.
- The end-user account assigned in this module is the same account used in Module 5 for the end-user perspective exercise.
