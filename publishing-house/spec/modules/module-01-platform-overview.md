# Module 01 — Exploring the Red Hat cloud extensions Platform

### Brief Overview

As the Sovereign Cloud Corp platform engineer, participants walk through a freshly deployed Red Hat cloud extensions environment before onboarding any tenants. They verify that the platform components in the `osac` namespace are healthy, explore the web UI, examine the Keycloak `osac` realm that governs tenant identity, and inspect the Kafka cluster that carries platform events. The module establishes a healthy baseline and an understanding of the platform's architecture before tenant management in Module 2.

### Audience and Time

**Audience**: Platform engineers and administrators responsible for operating Red Hat cloud extensions. Participants should have basic OpenShift CLI and console familiarity.

**Duration**: 15 min

### Learning Objectives

- Verify that all Red Hat cloud extensions operators and pods are running in the `osac` namespace
- Navigate the Red Hat cloud extensions web UI and identify its key sections
- Examine the Keycloak `osac` realm configuration that governs tenant identity
- Inspect the Kafka cluster to confirm the messaging infrastructure is healthy

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Verify the Red Hat cloud extensions namespace | 4 min |
| 2 | Explore the Red Hat cloud extensions web UI | 3 min |
| 3 | Examine the Keycloak realm configuration | 4 min |
| 4 | Inspect the Kafka cluster | 4 min |

### Detailed Steps

1. Verify the Red Hat cloud extensions namespace: in the *Terminal* tab, log in to OpenShift with `oc login` as cluster admin and confirm identity with `oc whoami` and `oc cluster-info`. Run `oc get pods -n osac` (all pods `Running` or `Completed`), `oc get csv -n osac` (all CSVs `Succeeded`), `oc get svc -n osac`, and `oc get routes -n osac` (routes for `osac-ui`, `keycloak`, and other fulfillment services).
2. Explore the Red Hat cloud extensions web UI: in the *cloud extensions* tab, log in with the platform admin credentials and locate the main sections — **Tenants** (only `shared` and `system` exist), **Catalog** (empty), **Projects** (only `default`), **Infrastructure** (Storage, Instance Types, External IP Pools, Bare metal instance types, Disk Images), **Networking** (Virtual Networks and Security Groups, empty until tenants exist), and **Secrets**.
3. Examine the Keycloak realm configuration: run `oc get pods -n keycloak` and `oc describe deployment keycloak-service -n keycloak`. In the *Keycloak* tab, log in as the Keycloak admin, select the **osac** realm, and review **Realm Settings** (session timeouts and token lifetimes). From the CLI, check `oc get endpoints keycloak -n keycloak` and the Keycloak ConfigMaps, then confirm the realm is served with `curl` against `{osac_keycloak_url}/realms/osac`.
4. Inspect the Kafka cluster: run `oc get kafka -n osac-kafka` and `oc describe kafka -n osac-kafka`, check broker pods with `oc get pods -n osac-kafka -l strimzi.io/kind=Kafka`, list `oc get kafkatopics -n osac-kafka` (note the `osac-` topics) and `oc get kafkausers -n osac-kafka`, and confirm the cluster status conditions show `Ready` is `True`.

### Key Takeaways

- Every platform operation flows through three core layers: identity (Keycloak), orchestration (osac-operator and fulfillment-service), and messaging (Kafka).
- Healthy CSVs are a prerequisite; a degraded operator means the platform cannot process tenant workload requests.
- The Keycloak `osac` realm is the trust anchor for all tenant authentication.
- Kafka is the event backbone for catalog requests, tenant lifecycle events, and workload status updates.

### Infrastructure Notes

- Participants use a pre-deployed Red Hat cloud extensions environment on OpenShift; no cluster setup is needed.
- Platform components run in the `osac` namespace, Keycloak in `keycloak`, and Kafka (Strimzi) in `osac-kafka`.
- The lab provides OpenShift cluster admin, Red Hat cloud extensions admin, and Keycloak admin credentials, plus *Terminal*, *cloud extensions*, and *Keycloak* tabs.
