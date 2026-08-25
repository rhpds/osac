# Module 05 — Virtual Machine Lifecycle

### Brief Overview

This capstone module brings together all prior work: participants order a virtual machine using the catalog item from Module 3, attach it to the network from Module 4, and manage it through its full lifecycle. Along the way, participants access the VM via the OCX serial console, attach a public IP address allocated from an admin-defined pool, perform stop/start/restart operations, and then clean up — experiencing the full OCX admin-to-user operational workflow.

### Audience and Time

**Audience**: OCX administrators and platform engineers; end-user perspective demonstrated in the public IP and cleanup sections.

**Prerequisites for this module**: Modules 01–04 complete; a tenant, catalog item, and virtual network are all in place.

**Duration**: 30 min

### Learning Objectives

- Provision a virtual machine within an OCX tenant by ordering from the service catalog using a specific InstanceType and network attachment
- Access the running VM via the OCX serial console without requiring direct cluster access
- Allocate a public IP address from a provider-defined pool and attach it to the VM to enable external connectivity
- Manage VM power state (stop, start, restart) using the OCX CLI and observe lifecycle state transitions

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Order a VM from the catalog | 10 min |
| 2 | Access the VM and attach a public IP | 8 min |
| 3 | VM lifecycle operations and cleanup | 12 min |

### Detailed Steps

**Section 1 — Order a VM from the catalog (10 min)**

1. As tenant admin, order a VM using the catalog item and networking from previous modules:
   ```bash
   osac create computeinstance \
     --name demo-vm \
     --catalog-item demo-linux-vm \
     --instance-type demo-small-1-2 \
     --boot-disk-size 10 \
     --run-strategy Always \
     --user-data "$(cat demo-vm-cloud-init.yaml)" \
     --network-attachment "subnet=${SUBNET_ID},security-groups=${SG_ID}"
   ```
2. Poll until STATE = **RUNNING** (typically 2–5 minutes as AAP provisions the KubeVirt VM):
   ```bash
   watch -n10 'osac get computeinstances | grep demo-vm'
   ```
3. Once RUNNING, verify the VM landed in the correct subnet namespace, not the hub namespace:
   ```bash
   oc get vm,vmi -n subnet-xxxxx | grep vm-     # KubeVirt VM is in the CUDN subnet namespace
   ```
4. Save the VM ID: `export VM_ID=$(osac get computeinstances | awk '/demo-vm/ {print $1}')`.

**Section 2 — Access the VM and attach a public IP (8 min)**

5. Access the running VM via the OCX serial console — no cluster-admin `oc` access required:
   ```bash
   osac console serial computeinstance demo-vm
   # login: osac-admin / password (set via cloud-init at order time)
   hostname; ip -4 addr show
   # Ctrl+] to disconnect
   ```
6. Confirm the VM has an internal IP in the subnet CIDR (`10.100.1.x`) and a default route through the CUDN gateway.
7. Allocate a public IP from the provider pool and attach it to the VM:
   ```bash
   osac create publicip --name demo-vm-public-ip --pool demo-public-pool
   # wait for STATE = ALLOCATED
   osac create publicipattachment --publicip demo-vm-public-ip --compute-instance demo-vm
   # wait for STATE = READY
   osac get computeinstances demo-vm   # PUBLIC IP ADDRESS now populated
   ```
8. Observe that the public IP is implemented as a MetalLB LoadBalancer Service in the subnet namespace — the admin-defined pool becomes an L2-advertised address on the lab network.

**Section 3 — VM lifecycle operations and cleanup (12 min)**

9. Stop the VM from the CLI (there is no `osac stop` verb — lifecycle is managed by editing `run_strategy`):
   ```bash
   osac edit computeinstance demo-vm   # set spec.run_strategy: Halted
   # watch: watch -n5 'osac get computeinstances demo-vm'  → STATE = STOPPED
   ```
10. Observe that while STOPPED, the KubeVirt VMI is absent but the VM PVC (disk) and networking resources are preserved.
11. Start the VM again:
    ```bash
    osac edit computeinstance demo-vm   # set spec.run_strategy: Always
    # wait for STATE = RUNNING; confirm internal IP is restored
    ```
12. Restart the VM in place (no re-order needed):
    ```bash
    osac edit computeinstance demo-vm   # set spec.restart_requested_at: "<current UTC ISO timestamp>"
    # wait for STATE = RUNNING again
    ```
13. Switch to the end-user (tenant user) account and open the VM creation wizard in the OCX UI to experience the consumer perspective — confirm the catalog item and instance type are visible.
14. Clean up tenant resources in the correct order (detach PublicIP → delete VM → delete PublicIP → delete SecurityGroup → delete Subnet → delete VirtualNetwork).

### Key Takeaways

- VM provisioning in OCX integrates the catalog item, instance type, and network attachment into a single order — all the admin-configured resources converge here.
- The OCX **serial console** (`osac console serial`) proxies through `osac-console-proxy` without exposing KubeVirt APIs directly to the tenant.
- **Public IPs** are a two-step process: allocate from an admin-defined pool, then attach to a VM. The platform provisions a MetalLB LoadBalancer Service in the subnet namespace to make the IP reachable.
- VM lifecycle (stop, start, restart) is driven by `spec.run_strategy` and `spec.restart_requested_at` — there are no `osac stop`/`osac start` subcommands; use `osac edit`.
- **Delete order matters**: detach PublicIP before deleting the VM; delete the VM before subnet/VNet. Reversing this order causes `FailedPrecondition` errors from the OCX API.
- Platform resources (NetworkClass, PublicIPPool, Catalog Item, InstanceType) persist after tenant cleanup — they are reused for the next provisioning cycle.

### Infrastructure Notes

- VM provisioning time depends on the AAP job queue; the lab environment is pre-tuned to minimize wait time.
- The end-user account must be assigned to the tenant (completed in Module 2) for the end-user perspective section to work.
- The `demo-public-pool` public IP pool is pre-configured by the platform — participants allocate from it; they do not create the pool.
- Assessment is observation-based: participants demonstrate the expected state in the OCX UI or via `osac get` CLI output.
