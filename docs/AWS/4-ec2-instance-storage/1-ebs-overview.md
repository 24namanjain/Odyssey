---
title: EBS Overview
tags: [aws, ec2, ebs, storage, block-storage]
---

# EBS Overview

## Console paths

> **EBS volumes:** `AWS Console` › `EC2` › `Storage` › `Volumes`

> **Attach volume:** `AWS Console` › `EC2` › `Storage` › `Volumes` › `Actions` › `Attach volume`

---

## What is EBS?

**Amazon EBS (Elastic Block Store)** provides network-attached block storage volumes for EC2 instances.

Think of EBS like a **network USB drive**:
- It is a separate resource from the instance
- It persists independently of instance stop/start
- You attach one or more volumes to an instance
- It lives in a specific **Availability Zone (AZ)**

An EC2 instance typically has **at least one EBS volume** (the root volume) and can have additional data volumes attached.

---

## Key characteristics

| Property | Detail |
|----------|--------|
| **Type** | Block storage (raw disk — you format with a filesystem) |
| **Scope** | Tied to one AZ |
| **Persistence** | Survives instance **stop/start** |
| **Attachment** | One instance at a time (except Multi-Attach volumes) |
| **Billing** | Charged for provisioned size, even if unused |

---

## Delete on instance termination

By default, the **root EBS volume is deleted** when the EC2 instance is **terminated**.

You can change this behavior:
- At launch time (Configure storage step)
- Later via volume settings

**Important distinction:**

| Instance action | EBS volume |
|-----------------|------------|
| **Stop** | Volume kept, reattached on start |
| **Terminate** | Volume deleted by default (configurable) |

> 📌 Stopping an instance does **not** delete EBS. Terminating might — depending on the *Delete on termination* flag.

---

## Common volume types (high level)

| Type | Use case |
|------|----------|
| **gp3 / gp2** | General-purpose SSD (boot volumes, most workloads) |
| **io1 / io2** | High IOPS, latency-sensitive databases |
| **st1** | Throughput-optimized HDD (big sequential reads) |
| **sc1** | Cold HDD (infrequent access) |

We used **gp3** when launching our learning instance (see [EC2 Phase 1](../3-ec2/1-creation-and-launch.md)).

---

## FAQs

**Q: Is EBS the same as instance storage?**
No. EBS is network-attached and persistent. [Instance Store](3-instance-store.md) is local hardware and ephemeral.

**Q: Can I detach a volume and attach it to another instance?**
Yes — as long as both instances are in the **same AZ**.

**Q: What happens to EBS when I stop my instance?**
The volume remains. You still pay for storage while stopped.
