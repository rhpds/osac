# Module 01 — Exploring the Red Hat cloud extensions Platform

### Brief Overview

The infrastructure team at Sovereign Cloud Corp has handed participants the keys to a freshly deployed Red Hat cloud extensions environment. Before onboarding tenants or provisioning workloads, participants verify that the platform components are healthy, explore the web UI, and understand how Keycloak and Kafka tie the system together. By the end of the module, they have a clear picture of the platform architecture and the confidence to continue.

### Audience and Time

**Audience**: Platform engineers and cloud architects responsible for operating Red Hat cloud extensions. Participants should have basic OpenShift CLI and console familiarity.

**Duration**: 10 min

### Learning Objectives

- Verify all Red Hat cloud extensions operators and pods are running in the `osac` namespace
- Navigate the Red Hat cloud extensions web UI and identify its key dashboard sections
- Examine the Keycloak realm configuration that governs tenant identity
- Inspect the Kafka cluster and confirm the messaging infrastructure is healthy

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Verify the Red Hat cloud extensions namespace | 3 min |
| 2 | Explore the Red Hat cloud extensions web UI | 2 min |
| 3 | Examine the Keycloak realm configuration | 3 min |
| 4 | Inspect the Kafka cluster | 2 min |

### Detailed Steps

1. Verify the Red Hat cloud extensions namespace: switch to the *Terminal* tab, log in to OpenShift with `oc login`, confirm identity with `oc whoami` and `oc cluster-info`, then check `oc get pods -n osac`, `oc get csv -n osac`, `oc get svc -n osac`, and `oc get routes -n osac`.
2. Explore the Red Hat cloud extensions web UI: switch to the *Red Hat cloud extensions* tab, log in with platform admin credentials, and locate **Tenants**, **Catalog**, **Projects**, **Infrastructure**, **Networking**, and **Secrets**.
3. Examine the Keycloak realm configuration: verify Keycloak pods and deployment status, log in to the *Keycloak* admin console, select the `osac` realm, review realm settings, inspect the Keycloak service endpoints and ConfigMaps, and confirm `{osac_keycloak_url}/realms/osac` is served.
4. Inspect the Kafka cluster: list and describe Kafka resources in `osac-kafka`, check broker pods, list `osac-` Kafka topics and KafkaUsers, and confirm the Kafka cluster `Ready` condition is `True`.

### Learning Outcomes Checkpoint

Participants should be able to answer:

- Which namespace contains all Red Hat cloud extensions platform components?
- Which Keycloak realm governs Red Hat cloud extensions tenant identities?
- What types of events does Kafka carry in the Red Hat cloud extensions platform?

### Key Takeaways

- Every platform operation in Red Hat cloud extensions flows through identity (Keycloak), orchestration (`osac-operator` and fulfillment-service), and messaging (Kafka).
- Healthy CSVs are a prerequisite; a degraded operator means the platform cannot process tenant or workload requests.
- The `osac` Keycloak realm is the trust anchor for all tenant authentication; its availability is non-negotiable for sovereign operations.

### Infrastructure Notes

- Participants use a pre-deployed Red Hat cloud extensions environment on OpenShift; no cluster setup is needed.
- Platform components run in the `osac` namespace, Keycloak runs in `keycloak`, and Kafka runs in `osac-kafka`.
- The lab provides OpenShift cluster admin, Red Hat cloud extensions admin, and Keycloak admin credentials, plus *Terminal*, *Red Hat cloud extensions*, and *Keycloak* tabs.
