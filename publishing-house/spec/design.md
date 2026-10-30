# Introduction to Red Hat cloud extensions

## Overview

This lab introduces participants to Red Hat cloud extensions — a sovereign cloud platform built on Red Hat OpenShift that provides multi-tenant self-service infrastructure with integrated identity management, an event backbone, and automated fulfillment. Participants take on the role of a Platform Engineer at Sovereign Cloud Corp, a European government services provider, and onboard a first government tenant, SAI Corp.

The lab covers the full operational workflow: verifying platform health, onboarding a tenant with federated SSO and role-based access control, publishing a virtual machine catalog so tenant users can deploy VMs on demand (VMaaS), and ordering hosted OpenShift clusters through the CaaS catalog — from both the platform administrator and the tenant user perspective.

## Target Audience

Platform Engineers and Cloud Architects responsible for deploying, configuring, and operating a Red Hat cloud extensions platform. Participants should be familiar with Red Hat OpenShift and Kubernetes concepts (namespaces, operators, custom resources), the `oc` CLI, YAML, and general cloud concepts such as tenants, virtual machines, and role-based access control.

## Prerequisites

- Familiarity with Red Hat OpenShift and Kubernetes concepts (projects, namespaces, operators, CRDs) and the `oc` CLI
- Reading and editing YAML, and intermediate Linux command-line usage
- Understanding of virtual machines, multi-tenancy, and role-based access control (RBAC)
- A Red Hat cloud extensions environment is provided — no installation required

## Learning Objectives

By the end of this lab, participants will be able to:

- Navigate and understand the Red Hat cloud extensions platform architecture and components
- Create and manage multi-tenant environments with storage
- Use the Red Hat cloud extensions user interface and the `osac` CLI to create catalog items and deploy workloads
- Provision virtual machines on demand through the VMaaS service catalog
- Order hosted OpenShift clusters using the CaaS catalog
- Verify platform health and tenant readiness

## Content Type

Hands-on lab

## Products & Technologies

- **Red Hat cloud extensions** — sovereign cloud platform providing multi-tenant self-service VMs and hosted OpenShift clusters (`osac` CLI)
- **Red Hat OpenShift Container Platform** — including OpenShift Virtualization, hosted control planes (HyperShift), and Metal3 bare-metal provisioning
- **Red Hat build of Keycloak** — tenant identity and federated SSO
- **Streams for Apache Kafka** — platform event backbone
- **Red Hat Ansible Automation Platform** — workload fulfillment

## Module Map

| Module | Title | Duration |
|--------|-------|----------|
| 1 | Exploring the Red Hat cloud extensions Platform | 10 min |
| 2 | Tenant Onboarding and Identity Management | 30 min |
| 3 | Virtual Machine as a Service (VMaaS) | 30 min |
| 4 | Cluster as a Service (CaaS) | 30 min |
| — | Total workshop | ~100 min |

**Module 1** covers platform orientation — verifying the platform components, exploring the web UI, and examining the Keycloak realm and Kafka cluster that underpin tenant identity and eventing.

**Modules 2–4** follow the natural admin workflow: onboard a tenant with federated SSO and role-based access, publish the VM catalog and deploy a virtual machine as a tenant administrator, and provision a bare-metal host to let tenants order hosted OpenShift clusters from the cluster catalog.

## Difficulty Level

Intermediate

## Environment

Participants access a pre-deployed Red Hat cloud extensions environment running on Red Hat OpenShift. The lab interface provides the Red Hat cloud extensions UI and a terminal with the `oc` and `osac` CLIs. Participants work as the platform administrator and as two tenant users, Alice (tenant administrator) and Bob (project viewer). No cluster setup or platform installation is required — the environment is ready when the lab starts.

## Infrastructure Requirements

- **Platform:** OCP
- **Cloud provider:** CNV
- **Topology:** Per-student (each student gets a dedicated Red Hat cloud extensions environment)
- **Cluster type:** Multinode
- **OCP version:** 4.22 (minimum)
- **Control plane:** 3 nodes, 16 vCPU, 32 GiB RAM each
- **Workers:** 2 nodes, each with 64 cores × 2 sockets = 128 vCPU, 128 GiB RAM, a 512 GiB root disk, and one 1024 GiB additional disk for LVMS (`/dev/vdb`)
- **Bastion:** 1 VM, 2 vCPU, 2 GiB RAM, 30 GiB root disk (inherited CNV defaults); attached to the cluster network at `10.10.10.1/24`
- **Bare-metal fabric (BMF):** 1 VM, 32 vCPU, 128 GiB RAM, 512 GiB root disk; attached to the cluster network at `10.10.10.2/24`, hosting the libvirt/Sushy environment used by Module 4
- **Storage:** External ODF workload plus LVMS enabled for tenant VM storage
- **Automation:** Ansible (`rhpds.sovereign_cloud.ocp4_workload_osac`), using the `full-ci` installer profile with BMF enabled
- **Catalog configuration:** [`rh1-2027/lb1657-sovereign-cloud-osac-cnv`](https://github.com/rhpds/agnosticv/tree/master/rh1-2027/lb1657-sovereign-cloud-osac-cnv) on AgnosticV `master`
- **OSAC release (dev/test):** `osac-release/v0.0.52`
- **OSAC CLI release (dev/test):** `fulfillment-service/v0.0.125`
- **Showroom content:** `rhpds/osac`; dev uses `main`, while test uses the snapshot tag `rh1-2027-lb1657-test-1.0.0`
- **Workshop duration:** ~100 min
- **Provisioning time:** Not verified by this configuration audit; measure a successful deployment before recording an estimate
- **AI/MaaS:** None
- **External services:** github.com, quay.io, mirror.openshift.com, rhdp-private.s3.us-east-1.amazonaws.com (AAP license)
- **Non-GA products:** None recorded in the spec; release support status was not verified by this configuration audit

### Infrastructure Review Notes

- Resource sizes above describe guest allocations, not CNV pod overhead or sandbox quotas.
- The Module 4 worker created inside the BMF host is nested lab capacity, separate from the two hub OpenShift workers.
- The catalog comment records an AAP license expiry of **2026-12-31**. Verify or renew the license for RH1 2027; the expiry was not independently checked.
- Configuration alignment does not establish successful provisioning, test execution, or infrastructure approval.

## Assessment Strategy (Optional)

Observation-based: participants demonstrate successful completion by showing the expected state in the Red Hat cloud extensions UI or CLI output. Modules 2–4 also provide a *Solve* button that automates the module so participants can catch up.

