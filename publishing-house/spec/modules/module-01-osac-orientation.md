# Module 01 — OCX Platform Orientation

### Brief Overview

This module introduces participants to the OpenShift Cloud Extensions (OCX) platform. Participants log in to the admin console, explore the main navigation areas, and examine the platform's NetworkClass model — the OCX mechanism that controls how tenant virtual networks are provisioned under the hood (CUDN overlay, MetalLB L2, or other backends). The module is intentionally short; its purpose is to orient participants and confirm the lab environment is functional before they tackle hands-on tasks.

### Audience and Time

**Audience**: OCX administrators and platform engineers. Participants should have basic OpenShift console familiarity.

**Duration**: 15 min

### Learning Objectives

- Identify the main sections of the OCX administrative console and explain the distinction between provider admin and tenant admin roles
- Explain the NetworkClass model and why CUDN (`cudn_net`) is the default for tenant virtual networks on this platform
- Verify that both the admin account and end-user account are accessible and the lab environment is ready to proceed

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Log in and explore the OCX console | 5 min |
| 2 | Review NetworkClass and platform capabilities | 5 min |
| 3 | Verify lab environment readiness | 5 min |

### Detailed Steps

1. Log in to the OCX administrative console using the admin credentials provided in the lab environment.
2. Identify the main navigation sections: Tenants, Catalog Items, Instance Types, Virtual Networks, and Virtual Machines.
3. Navigate to **Networking → Network Classes** and review the available network implementations.
4. Observe that **CUDN Network Implementation** (`cudn_net`) is the default — tenant VirtualNetworks use OVN-backed isolated overlays by default.
5. From the lab terminal, run `osac get networkclass` to see all available implementations (CUDN, MetalLB L2, etc.) and confirm CUDN is marked as default.
6. Log in to the tenant user account to confirm it is accessible — then return to the admin account.
7. Confirm the lab environment is healthy and ready to proceed to Module 2.

### Key Takeaways

- OCX is built on Red Hat OpenShift and exposes a cloud-native API for multi-tenant VM infrastructure.
- OCX separates roles: the **provider admin** manages platform resources (NetworkClasses, IP pools, catalog items, instance types); **tenant admins** consume them to provision VMs.
- A **NetworkClass** is the OCX equivalent of a Kubernetes StorageClass for networking — it determines which backend (CUDN, MetalLB, Netris) provisions the overlay when a tenant creates a VirtualNetwork.
- CUDN (`cudn_net`) uses OVN Kubernetes — tenant VMs get isolated L2 networks without tenants needing to know the plumbing.

### Infrastructure Notes

- Participants access a pre-deployed OCX environment; no cluster setup is needed.
- The `osac` CLI is pre-installed and configured in the lab terminal.
- Both an admin credential and a tenant credential are provided in the lab environment details.
