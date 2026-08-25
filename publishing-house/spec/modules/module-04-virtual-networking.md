# Module 04 — Virtual Networking

### Brief Overview

OCX enforces tenant isolation through virtual networking. This module covers creating a virtual network scoped to the lab tenant, partitioning it with subnetworks, and applying security group policies that control traffic to and from virtual machines. The network infrastructure built here is attached to VMs in Module 5.

### Audience and Time

**Audience**: OCX administrators and platform engineers responsible for designing and implementing tenant network topology and security policy.

**Prerequisites for this module**: Module 02 complete; a tenant exists. Module 03 is independent of networking.

**Duration**: 25 min

### Learning Objectives

- Create a virtual network scoped to an OCX tenant
- Configure subnetworks with defined IP address ranges for workload segmentation
- Implement security group policies to control inbound and outbound traffic between VMs
- Verify network isolation between tenants within the OCX platform

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Create a virtual network | 8 min |
| 2 | Add and configure subnetworks | 9 min |
| 3 | Define and attach security group policies | 8 min |

### Detailed Steps

1. Navigate to the Virtual Networks section of the OCX admin console and create a new virtual network scoped to the lab tenant.
2. Define a subnetwork within the virtual network, specifying a CIDR range and any gateway or DNS settings.
3. Create a security group and configure inbound and outbound rules appropriate for the lab workload (e.g., allow SSH, restrict inter-tenant traffic).
4. Attach the security group to the virtual network or subnetwork.
5. Verify the network configuration is complete and review how the platform enforces isolation from other tenants.

### Key Takeaways

- Virtual networks in OCX provide isolated Layer 2 connectivity scoped to a single tenant.
- Subnetworks partition the tenant's address space and can reflect functional or organizational separation of workloads.
- Security groups provide stateful firewall enforcement, controlling which traffic is permitted to reach tenant VMs.
- Network resources are tenant-scoped by design — cross-tenant communication is not permitted without explicit policy, ensuring sovereign isolation.

### Infrastructure Notes

- Network CIDR ranges used in the lab should be non-overlapping with the underlying OpenShift cluster network.
- The virtual network and subnetwork created here are selected when provisioning the VM in Module 5.
