# Open Sovereign AI Cloud: Tenant Administration and VM Lifecycle

## Overview

This lab introduces participants to the Open Sovereign AI Cloud (OSAC) platform — a sovereign cloud solution built on Red Hat OpenShift that provides multi-tenant virtual machine infrastructure with integrated identity management and networking. Participants take on the role of an OSAC administrator to set up and operate the platform, then switch to the end-user perspective to consume those resources.

The lab covers the full operational workflow: creating and managing tenants, building VM templates, configuring virtual networks and security policies, and provisioning virtual machines — giving participants the hands-on skills to operate an OSAC environment from both the admin and user perspective.

## Target Audience

OSAC administrators, platform engineers, and operations teams responsible for deploying, configuring, and operating OSAC environments. Participants should have basic familiarity with Red Hat OpenShift (navigating the console, understanding namespaces) and general cloud concepts such as tenants, virtual networks, and virtual machines. Prior knowledge of Sovereign Cloud concepts is helpful but not required.

## Prerequisites

- Basic familiarity with Red Hat OpenShift (console navigation, namespaces)
- Understanding of general cloud concepts: tenants, virtual networks, virtual machines
- An OSAC environment is provided — no installation required

## Learning Objectives

By the end of this lab, participants will be able to:

- Create and manage OSAC tenants using the admin interface
- Build and publish VM templates for use within an OSAC tenant
- Configure virtual networks, subnetworks, and security groups for tenant isolation
- Provision and manage virtual machines within an OSAC tenant environment
- Explore OSAC as an end user to request and access VM resources

## Content Type

Hands-on lab

## Products & Technologies

- **Open Sovereign AI Cloud (OSAC)** — sovereign cloud platform providing multi-tenant VM infrastructure

## Module Map

| Module | Title | Duration |
|--------|-------|----------|
| 1 | OSAC Platform Orientation | 10 min |
| 2 | Tenant Administration | 20 min |
| 3 | VM Templates | 15 min |
| 4 | Virtual Networking | 20 min |
| 5 | Virtual Machine Lifecycle | 20 min |
| — | Total hands-on | ~85 min |
| — | Intro / presentation | ~5 min |
| — | Total lab | ~90 min |

**Module 1** covers platform orientation — exploring the OSAC UI, understanding the architecture, and confirming the lab environment works. Short and fast (10 min) so participants spend most of their time on hands-on tasks.

**Modules 2–5** follow the natural admin workflow: first create the organizational unit (tenant), then add the resources it can use (templates, networks), then provision actual workloads (VMs). Module 5 also includes the end-user perspective — switching roles to show how a tenant user requests and accesses a VM.

## Difficulty Level

Intermediate

## Environment

Participants access a pre-deployed OSAC environment running on Red Hat OpenShift. The lab provides both an admin account and an end-user account to demonstrate both administrative and consumer perspectives. No cluster setup or OSAC installation is required — the environment is ready when the lab starts.

## Infrastructure Requirements

- **Platform:** OCP
- **Cloud provider:** CNV
- **Topology:** Per-student (each student gets a dedicated OSAC environment)
- **Cluster type:** Multinode
- **OCP version:** 4.22 (minimum)
- **Control plane:** 3 nodes, 16 vCPU, 32GB RAM each
- **Workers:** 2 nodes (default; up to 5), 64 vCPU, 128GB RAM, 512GB root disk, 2×2TB extra disks each
- **Automation:** Ansible (`rhpds.sovereign_cloud.ocp4_workload_osac`)
- **Provisioning time:** ~55 min total (~25 min cluster + ~30 min OSAC deployment)
- **AI/MaaS:** TBD
- **External services:** github.com, quay.io, mirror.openshift.com, rhdp-private.s3.us-east-1.amazonaws.com (AAP license)
- **Non-GA products:** None

## Assessment Strategy (Optional)

Observation-based: participants demonstrate successful completion by showing the expected state in the OSAC UI or CLI output. No automated solve/validate scripts are required for this classic showroom lab.
