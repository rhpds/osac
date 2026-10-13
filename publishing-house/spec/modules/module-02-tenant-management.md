# Module 02 — Tenant Administration

### Brief Overview

Tenants are the primary organizational boundary in OCX. This module walks participants through creating and configuring a tenant using the OCX admin interface and CLI. OCX uses a **two-layer tenant model**: a fulfillment tenant (managed by the OCX API) and a Hub Tenant CR (a Kubernetes custom resource the operator uses to provision VMs). Participants create both layers, configure resource quotas, assign users, and verify the tenant is ready for downstream provisioning.

### Audience and Time

**Audience**: OCX administrators and platform engineers responsible for setting up and operating multi-tenant environments.

**Prerequisites for this module**: Module 01 complete; admin console and `osac` CLI accessible.

**Duration**: 25 min

### Learning Objectives

- Create an OCX tenant using both the fulfillment API (`osac create -f`) and the Hub Tenant CR (`oc apply`)
- Explain the two-layer tenant model and why both layers are required for VM provisioning
- Configure tenant resource quotas and assign user accounts with appropriate role bindings
- Verify that a newly created tenant is synchronized and ready for VM provisioning

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Create the fulfillment tenant and Hub Tenant CR | 10 min |
| 2 | Configure quotas and review storage class binding | 9 min |
| 3 | Assign users and verify tenant state | 6 min |

### Detailed Steps

1. Log in to the OCX CLI as tenant admin:
   ```bash
   osac login --insecure --address "${FULFILLMENT_PUBLIC}" \
     --flow password --user tenant_admin --password <password>
   ```
2. Create the fulfillment tenant by applying a Tenant manifest:
   ```bash
   osac create -f tenant.yaml   # type: osac.private.v1.Tenant
   osac get tenants             # verify STATUS = SYNCED
   ```
3. Create the Hub Tenant CR in OpenShift (required for VM provisioning):
   ```bash
   oc apply -f hub-tenant.yaml  # kind: Tenant, apiVersion: osac.openshift.io/v1alpha1
   oc get tenant <name> -n osac-<env>
   ```
   Wait until PHASE = **Ready** (~30–120s).
4. Verify the Hub Tenant CR has resolved storage classes:
   ```bash
   oc get tenant <name> -n osac-<env> -o jsonpath='{.status.storageClasses}'
   ```
   The storage class list must be non-empty before VM provisioning can succeed.
5. Configure tenant resource quotas (CPU, memory, storage) in the admin console.
6. Assign the end-user account to the tenant with an appropriate role binding.
7. Review the completed tenant record and confirm it appears correctly in both `osac get tenants` and the OCX console.

### Key Takeaways

- OCX uses a **two-layer tenant model**: the fulfillment tenant governs API-level resources (virtual networks, VMs, public IPs); the Hub Tenant CR is consumed by the `osac-operator` when provisioning VMs via AAP.
- A tenant with PHASE=Ready but empty `status.storageClasses` will fail VM provisioning — always verify storage class binding after tenant creation.
- The `Tenant` type changed from `osac.private.v1.Organization` to `osac.private.v1.Tenant` — use `osac get tenants` not `osac get organizations` on current builds.
- Role-based access control separates administrative operations from end-user consumption.

### Infrastructure Notes

- The tenant created in this module is used throughout Modules 3, 4, and 5 — use consistent naming.
- The end-user account assigned in this module is the same account used in Module 5 for the end-user perspective exercise.
- Storage class labels (`osac.openshift.io/tenant=Default`, `osac.openshift.io/storage-tier=default`) must be present on the cluster's default storage class for the Hub Tenant CR to resolve storage tiers.
