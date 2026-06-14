---
title: EBS Snapshots & AMI
tags: [aws, ec2, ebs, snapshots, ami, storage]
---

# EBS Snapshots & AMI

## Console paths

> **EBS snapshots:** `AWS Console` › `EC2` › `Storage` › `Snapshots`

> **Create snapshot:** `AWS Console` › `EC2` › `Storage` › `Volumes` › select volume › `Actions` › `Create snapshot`

> **Create AMI from instance:** `AWS Console` › `EC2` › `Instances` › select instance › `Actions` › `Images and templates` › `Create image`

> **Launch from AMI:** `AWS Console` › `EC2` › `Images` › `AMIs` › select AMI › `Launch instance from AMI`

---

## EBS Snapshots

A **snapshot** is a point-in-time backup of an EBS volume, stored incrementally in **Amazon S3** (you manage it through the EC2 console, not S3 directly).

**Use cases:**
- Backup before risky changes
- Clone a volume to another AZ or region
- Create a new (larger) volume from a snapshot
- Build an AMI for repeatable deployments

**Flow:**
```
EBS Volume  →  Create Snapshot  →  Restore new Volume (or create AMI)
```

Snapshots are **incremental** — only changed blocks are stored after the first snapshot, which saves cost over time.

---

## AMI (Amazon Machine Image)

An **AMI** is a pre-packaged image used to launch EC2 instances. It includes:
- OS configuration
- Pre-installed software (optional)
- EBS snapshot(s) of the root (and optionally data) volumes

**Key properties:**
- **Region-specific** — an AMI in `us-east-1` cannot launch directly in `eu-west-1` (copy it first)
- **Faster boot & config** — bake software into the AMI instead of installing on every launch
- **Backed by EBS** — most modern AMIs use EBS-backed storage

---

## Creating an AMI from a running instance

After configuring an instance exactly how you want it:

1. Select the running instance
2. `Actions` → `Images and templates` → `Create image`
3. Fill in name, description, and reboot behavior
4. AWS creates snapshots and registers a new AMI

> 📌 Creating an image may reboot the instance depending on the option you choose — plan accordingly.

---

## Launching an instance from an AMI

1. Go to **AMIs** under **Images**
2. Select your AMI
3. Choose **Launch instance from AMI**
4. Configure instance type, security group, etc. (same flow as a normal launch)

This is how you scale identical environments — web servers, workers, etc.

---

## Snapshots vs AMIs

| | Snapshot | AMI |
|---|----------|-----|
| **What it is** | Backup of a volume | Launch template for instances |
| **Primary use** | Backup, restore, migrate | Repeatable instance provisioning |
| **Contains** | Block data only | OS + volume metadata + launch permissions |

An AMI is built **on top of** EBS snapshots.

---

## FAQs

**Q: Are snapshots stored in S3?**
Yes, internally — but you interact with them through the EC2 console.

**Q: Can I share an AMI across accounts?**
Yes, via launch permissions.

**Q: What happens if I delete a snapshot that an AMI depends on?**
The AMI becomes unusable. Delete AMIs before orphaned snapshots, or vice versa — plan carefully.
