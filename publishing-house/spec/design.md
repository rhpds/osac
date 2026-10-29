# Introduction to Red Hat cloud extensions

## Overview

This lab introduces participants to Red Hat cloud extensions — a sovereign cloud platform built on Red Hat OpenShift that provides multi-tenant self-service infrastructure with integrated identity management, an event backbone, and automated fulfillment. Participants take on the role of a Platform Engineer at Sovereign Cloud Corp, a European government services provider, and onboard a first government tenant, SAI Corp.

The lab covers the full operational workflow: verifying platform health, onboarding a tenant with federated SSO and role-based access control, publishing a virtual machine catalog so tenant users can deploy VMs on demand (VMaaS), and provisioning bare-metal capacity so tenants can order hosted OpenShift clusters (CaaS) — from both the platform administrator and the tenant user perspective.

## Target Audience

Platform Engineers and Cloud Architects responsible for deploying, configuring, and operating a Red Hat cloud extensions platform. Participants should be familiar with Red Hat OpenShift and Kubernetes concepts (namespaces, operators, custom resources), the `oc` CLI, YAML, and general cloud concepts such as tenants, virtual machines, and role-based access control.

## Prerequisites

- Familiarity with Red Hat OpenShift and Kubernetes concepts (projects, namespaces, operators, CRDs) and the `oc` CLI
- Reading and editing YAML, and intermediate Linux command-line usage
- Understanding of virtual machines, multi-tenancy, and role-based access control (RBAC)
- A Red Hat cloud extensions environment is provided — no installation required

## Learning Objectives

By the end of this lab, participants will be able to:

- Verify the health of the Red Hat cloud extensions platform components, including the `osac` operators, Keycloak realm, and Kafka cluster
- Create a tenant and onboard its users through federated SSO with just-in-time provisioning
- Assign tenant-admin and project viewer roles and verify RBAC enforcement
- Publish a `ComputeInstanceCatalogItem` and deploy a virtual machine from the catalog as a tenant administrator
- Order a hosted OpenShift cluster on bare-metal capacity as a tenant using the `osac` CLI

## Content Type

Hands-on lab

## Products & Technologies

- **Red Hat cloud extensions** — sovereign cloud platform providing multi-tenant self-service VMs and clusters (`osac` CLI)
- **Red Hat OpenShift Container Platform** — including OpenShift Virtualization, hosted control planes (HyperShift), and Metal3 bare-metal provisioning
- **Red Hat build of Keycloak** — tenant identity and federated SSO
- **Streams for Apache Kafka** — platform event backbone
- **Red Hat Ansible Automation Platform** — workload fulfillment

## Module Map

| Module | Title | Duration |
|--------|-------|----------|
| 1 | Exploring the Red Hat cloud extensions Platform | 15 min |
| 2 | Tenant Onboarding and Identity Management | 25 min |
| 3 | Virtual Machine as a Service (VMaaS) | 20 min |
| 4 | Cluster as a Service (CaaS) | 25 min |
| — | Total hands-on | ~85 min |
| — | Intro / presentation | ~5 min |
| — | Total lab | ~90 min |

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
- **Control plane:** 3 nodes, 16 vCPU, 32GB RAM each
- **Workers:** 2 nodes (default; up to 5), 64 vCPU, 128GB RAM, 512GB root disk, 2×2TB extra disks each
- **Automation:** Ansible (`rhpds.sovereign_cloud.ocp4_workload_osac`)
- **Provisioning time:** ~110 min total (~75 min base cluster + ~25 min Red Hat cloud extensions deployment)
- **AI/MaaS:** None
- **External services:** github.com, quay.io, mirror.openshift.com, rhdp-private.s3.us-east-1.amazonaws.com (AAP license)
- **Non-GA products:** None

## Assessment Strategy (Optional)

Observation-based: participants demonstrate successful completion by showing the expected state in the Red Hat cloud extensions UI or CLI output. Modules 2–4 also provide a *Solve* button that automates the module so participants can catch up.

