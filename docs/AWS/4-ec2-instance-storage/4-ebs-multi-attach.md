---
title: EBS Multi-Attach
tags: [aws, ec2, ebs, storage, multi-attach]
---

# EBS Multi-Attach

## Console paths

> **Enable Multi-Attach:** `AWS Console` › `EC2` › `Storage` › `Volumes` › `Create volume` › enable *Multi-Attach enabled* (io1/io2 only)

> **Attach to second instance:** `AWS Console` › `EC2` › `Storage` › `Volumes` › select volume › `Actions` › `Attach volume`

---

## What is EBS Multi-Attach?

Normally, one EBS volume attaches to **one EC2 instance** at a time.

**EBS Multi-Attach** (available on **io1** and **io2** volumes) lets you attach the **same volume to multiple EC2 instances simultaneously** — but only within the **same Availability Zone**.

Use case: clustered applications that need shared block storage (e.g. some database or cluster filesystem setups).

---

## Limitations

| Limit | Detail |
|-------|--------|
| **Max instances** | Up to **16** EC2 instances per volume |
| **Same AZ only** | All instances must be in the same AZ as the volume |
| **Volume types** | **io1** and **io2** only |
| **Filesystem** | Must use a **cluster-aware filesystem** (standard ext4/xfs on multiple nodes without clustering = data corruption) |

> ⚠️ Multi-Attach does **not** provide file locking. Your application or filesystem must coordinate concurrent access.

---

## When to use Multi-Attach vs EFS

| Need | Choose |
|------|--------|
| Shared **block** storage, same AZ, cluster FS | EBS Multi-Attach |
| Shared **file** storage, multi-AZ, Linux | [EFS](5-efs-overview.md) |
| Single instance disk | Standard EBS |

---

## FAQs

**Q: Can I use Multi-Attach with gp3?**
No — only provisioned IOPS SSD (`io1`/`io2`).

**Q: What filesystems support clustering?**
Examples include GFS2, OCFS2 — not default single-node ext4. Always match FS to your cluster software.
