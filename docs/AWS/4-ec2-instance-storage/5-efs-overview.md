---
title: EFS Overview
tags: [aws, ec2, efs, storage, nfs, file-storage]
---

# EFS Overview

## Console paths

> **EFS file systems:** `AWS Console` › `Amazon EFS` › `File systems`

> **Create file system:** `AWS Console` › `Amazon EFS` › `File systems` › `Create file system`

> **Mount on EC2:** `AWS Console` › `Amazon EFS` › `File systems` › select file system › `Attach`

---

## What is EFS?

**Amazon EFS (Elastic File System)** is a **managed NFS (Network File System)** that multiple EC2 instances can mount at the same time.

Unlike EBS:
- **Shared** across many instances
- **Multi-AZ** by default (high availability)
- **Elastic** — grows and shrinks automatically as you add/remove files
- **File storage** (directories and files), not raw block devices

Think of EFS as a **shared network drive** for your fleet of Linux instances.

---

## Key characteristics

| Property | Detail |
|----------|--------|
| **Protocol** | NFSv4 |
| **OS support** | **Linux-based AMIs only** (not Windows) |
| **Availability** | Regional, multi-AZ |
| **Cost** | Pay for storage used — generally **more expensive** than EBS for equivalent size |
| **Performance modes** | Set at **creation time** (cannot change later) |

---

## Performance modes

Choose when creating the file system:

| Mode | Best for |
|------|----------|
| **General Purpose** (default) | Web servers, CMS, general file sharing — low latency |
| **Max I/O** | Large scale, highly parallel workloads — higher latency, higher throughput |

> 📌 Pick performance mode at creation. Plan workload type upfront.

---

## Mounting EFS on EC2

After creating a file system:

1. Create **mount targets** in your subnets (EFS wizard can do this)
2. Ensure **security groups** allow NFS traffic (port **2049**) between EC2 and EFS
3. On the EC2 instance, install `amazon-efs-utils` and mount using the EFS DNS name

The console **Attach** instructions give the exact mount command for your file system.

---

## EFS vs EBS vs Instance Store

| | EFS | EBS | Instance Store |
|---|-----|-----|----------------|
| **Type** | File (NFS) | Block | Block |
| **Multi-instance** | ✅ Yes | ❌ No* | ❌ No |
| **Multi-AZ** | ✅ Yes | ❌ Per AZ | ❌ Local only |
| **Durability** | High | High | None |

\* *Except [Multi-Attach](4-ebs-multi-attach.md).*

---

## FAQs

**Q: Can Windows EC2 mount EFS?**
No — EFS is Linux-compatible only.

**Q: Do I size EFS in advance?**
No — it scales automatically. You pay for what you store.

**Q: EFS vs S3 for shared files?**
EFS is POSIX filesystem (apps read/write like local disk). S3 is object storage — different access model.
