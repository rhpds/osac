# Module 02 — Tenant Onboarding and Identity Management

### Brief Overview

Sovereign Cloud Corp onboards a new government agency client, SAI Corp. Participants create the `sai-corp` tenant in Red Hat cloud extensions and verify the automatically provisioned Keycloak organization, namespace, and break-glass account. They then set up a Keycloak realm that simulates SAI Corp's corporate identity provider, register it for federated SSO, onboard Alice and Bob through device flow login, assign Alice as tenant admin and Bob as a project viewer, and prove that RBAC lets a viewer read but not delete.

### Audience and Time

**Audience**: Platform administrators and platform engineers responsible for onboarding tenants and managing identity and access in multi-tenant environments.

**Prerequisites for this module**: Module 01 complete; Red Hat cloud extensions console and `osac` CLI accessible.

**Duration**: 25 min

### Learning Objectives

- Create a tenant and verify automatic provisioning of its Keycloak organization, namespace, and break-glass account
- Configure an external identity provider for federated SSO
- Onboard users through SSO and trigger just-in-time (JIT) user provisioning
- Assign tenant-admin and project viewer roles using RoleBindings and ProjectMemberships
- Verify RBAC enforcement by confirming a viewer can list projects but cannot delete them

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Create a tenant and verify onboarding | 5 min |
| 2 | Set up a corporate identity provider | 7 min |
| 3 | Onboard tenant users via SSO | 6 min |
| 4 | Assign roles and manage projects | 5 min |
| 5 | Verify RBAC enforcement | 2 min |

### Detailed Steps

1. Create a tenant and verify onboarding:
   - Create `${HOME}/yaml` and log in to the internal fulfillment API as platform administrator with `osac --config $HOME/admin login --private ...`.
   - In the Red Hat cloud extensions console, go to Administration -> Tenants and create the `sai-corp` tenant; save the one-time break-glass password and wait for `Synced`.
   - Verify the break-glass credentials secret with `osac get tenant sai-corp -o json`, the Keycloak organization through the Keycloak admin REST API, and the namespace with `oc get ns sai-corp`.
2. Set up a corporate identity provider:
   - Using the Keycloak REST API (`curl`), create the `sai-corp-idp` realm, extend its session limits to 24 hours, create the `osac-federation` OIDC client, and create users `alice` and `bob`.
   - Log in to the console as the `sai-corp-osac-break-glass` user and change the password.
   - Log in to the CLI as the break-glass user and create the `idp-client-secret` value secret with `osac create secret`; verify it with `osac get secret`.
   - In the console, create the `sai-corp` identity provider (client ID, client secret, issuer, authorization and token URLs) and verify `IDENTITY_PROVIDER_PHASE_READY` with `osac get identityprovider`.
3. Onboard tenant users via SSO:
   - Log in as Alice with `osac login --flow device`, completing the login in a fresh incognito window through SAI Corp Corporate SSO.
   - Confirm identity with `osac whoami`, trigger JIT provisioning with `osac get projects`, and observe that `osac get users` returns `PermissionDenied`.
   - Repeat the device flow login, `whoami`, and `get projects` for Bob.
   - Verify that Alice, Bob, and the break-glass account are members of the SAI Corp Keycloak organization.
4. Assign roles and manage projects:
   - As the break-glass user in the console, create the `sai-corp-tenant-admin-binding` RoleBinding assigning the Tenant Administrator role to Alice; verify `ROLE_BINDING_STATE_READY` with `osac get rolebinding`.
   - Confirm Alice has `tenant-admin` with `osac whoami` and can now run `osac get users`.
   - As Alice, create the `sai-corp-default-project` project with `osac create -f` and list it with `osac get projects`.
   - As Alice, create the `bob-viewer` ProjectMembership granting Bob `PROJECT_MEMBERSHIP_ROLE_VIEWER` and verify it with `osac get projectmemberships`.
5. Verify RBAC enforcement:
   - As Bob, confirm `tenant-admin` is absent from `osac whoami` and that `osac get projects` lists the project.
   - Run `osac delete project sai-corp-default-project` as Bob and confirm it fails with `PermissionDenied`.

### Key Takeaways

- Tenant creation is fully automated: the platform provisions the Keycloak organization, namespace, and break-glass account in one operation.
- Identity federation means corporate users never receive platform passwords; authentication flows through their existing IdP.
- A user's platform record is created just in time on their first real API call after login; `osac whoami` reads only the local token.
- RBAC operates at two levels: RoleBindings for tenant-wide authority and ProjectMemberships for project-scoped access.
- The break-glass account provides emergency access when the corporate IdP is unavailable; its password must be saved at creation time.

### Infrastructure Notes

- Requires the Red Hat cloud extensions console, the `osac` CLI, `oc`, `curl`, and `jq` in the terminal, plus Keycloak admin credentials for the REST API steps.
- Device flow logins are completed in a separate incognito browser window outside the Showroom interface.
- The `sai-corp` tenant, the users Alice and Bob, and their CLI configurations (`$HOME/admin`, `$HOME/alice`, `$HOME/bob`) are reused in later modules.
- A Solve button creates the tenant, identity provider, roles, and memberships for participants who skip the exercises.
