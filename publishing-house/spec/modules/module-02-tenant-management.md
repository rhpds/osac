# Module 02 — Tenant Onboarding and Identity Management

### Brief Overview

Sovereign Cloud Corp has signed a new government agency client: SAI Corp. Participants onboard SAI Corp as a tenant using the `osac` CLI, configure SSO federation through a Keycloak realm that simulates the corporate identity provider, and prove that role-based access control enforces the right boundaries: Alice receives tenant-admin authority and Bob receives read-only project access.

### Audience and Time

**Audience**: Platform administrators and platform engineers responsible for onboarding tenants and managing identity and access in multi-tenant environments.

**Prerequisites for this module**: Module 01 complete; Red Hat cloud extensions console and `osac` CLI accessible.

**Duration**: 30 min

### Learning Objectives

- Create a tenant and verify automatic Keycloak organization and namespace provisioning
- Configure an external identity provider for federated SSO
- Onboard users through SSO and understand JIT user provisioning
- Assign tenant-admin and project viewer roles using RoleBindings and ProjectMemberships
- Verify RBAC enforcement: viewers can read but cannot delete

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Create a tenant and verify onboarding | 6 min |
| 2 | Set up a corporate identity provider | 10 min |
| 3 | Onboard tenant users via SSO | 6 min |
| 4 | Assign roles and manage projects | 5 min |
| 5 | Verify RBAC enforcement | 3 min |

### Detailed Steps

1. Create a tenant and verify onboarding:
   - Create `${HOME}/yaml` for workshop YAML files.
   - Log in to the internal fulfillment API as platform administrator using `osac --config $HOME/admin login --private`.
   - In the Red Hat cloud extensions console, create the `sai-corp` tenant, save the one-time break-glass password, and wait for the tenant to show `Synced`.
   - Verify the break-glass credentials secret with `osac --config $HOME/admin get tenant sai-corp -o json`, confirm the Keycloak organization via the Keycloak admin REST API, and confirm the namespace with `oc get ns sai-corp`.
2. Set up a corporate identity provider:
   - Use the Keycloak REST API to obtain an admin token.
   - Create the `sai-corp-idp` realm, extend its session limits to 24 hours, create the `osac-federation` OIDC client, and create users `alice` and `bob`.
   - Log in as the `sai-corp-osac-break-glass` user, change the password, and create the `idp-client-secret` value secret with `osac create secret`.
   - In the console, create the `sai-corp` identity provider and verify `IDENTITY_PROVIDER_PHASE_READY` with `osac get identityprovider`.
3. Onboard tenant users via SSO:
   - Log in as Alice with `osac login --flow device`, complete the login in an incognito browser through SAI Corp Corporate SSO, run `osac whoami`, and trigger JIT provisioning with `osac get projects`.
   - Repeat the device flow login, `whoami`, and `get projects` for Bob.
   - Verify Alice, Bob, and the break-glass account are members of the SAI Corp Keycloak organization.
4. Assign roles and manage projects:
   - As the break-glass user, create the `sai-corp-tenant-admin-binding` RoleBinding that assigns Alice the Tenant Administrator role.
   - Confirm Alice has `tenant-admin`, then create the `sai-corp-default-project` project.
   - As Alice, create the `bob-viewer` ProjectMembership granting Bob `PROJECT_MEMBERSHIP_ROLE_VIEWER` and verify it.
5. Verify RBAC enforcement:
   - As Bob, confirm `tenant-admin` is absent from `osac whoami` and that `osac get projects` lists the project.
   - Attempt to delete `sai-corp-default-project` as Bob and confirm the request fails with `PermissionDenied`.

### Learning Outcomes Checkpoint

Participants should have:

- Created the `sai-corp` tenant and saved the one-time break-glass credentials
- Verified automatic Keycloak organization and tenant namespace provisioning
- Created a secret for the OIDC client
- Configured a corporate identity provider for federated SSO
- Onboarded Alice and Bob through device flow login with JIT user provisioning
- Assigned Alice as tenant-admin using a RoleBinding
- Created a project and granted Bob viewer access via ProjectMembership
- Confirmed RBAC enforcement: Bob can list but cannot delete resources

### Key Takeaways

- Tenant creation is fully automated: the platform handles Keycloak organization, namespace, and emergency access provisioning in a single operation.
- Identity federation means corporate users never receive platform passwords; authentication flows through their existing IdP.
- RBAC operates at two levels: RoleBindings for tenant-wide authority and ProjectMemberships for project-scoped access.
- The break-glass account provides emergency access when the corporate IdP is unavailable; its password must be saved at creation time.

### Infrastructure Notes

- Requires the Red Hat cloud extensions console, the `osac` CLI, `oc`, `curl`, and `jq`, plus Keycloak admin credentials for REST API steps.
- Device flow logins are completed in a separate incognito browser window outside the Showroom interface.
- The `sai-corp` tenant, Alice, Bob, and their CLI configurations (`$HOME/admin`, `$HOME/alice`, `$HOME/bob`) are reused in later modules.
- The module Solve button creates the tenant, identity provider, roles, and memberships for participants who skip the exercises.
