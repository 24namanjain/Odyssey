---
title: EC2 Instance Storage
tags: [aws, ec2, storage, ebs, efs, guides]
---

# EC2 Instance Storage

Overview of storage options for EC2 instances — from block volumes to shared file systems.

## Topics

| Topic | What it covers |
|-------|----------------|
| [EBS Overview](1-ebs-overview.md) | Elastic Block Store — network-attached disks |
| [EBS Snapshots & AMI](2-ebs-snapshots-and-ami.md) | Backups, images, and launching from AMIs |
| [EC2 Instance Store](3-instance-store.md) | Ephemeral high-IOPS local storage |
| [EBS Multi-Attach](4-ebs-multi-attach.md) | Sharing one volume across instances |
| [EFS Overview](5-efs-overview.md) | Elastic File System — shared NFS storage |

## Quick comparison

| Storage | Type | Durability | Shared across instances | Typical use |
|---------|------|------------|-------------------------|-------------|
| **EBS** | Block | Persistent | No (one instance per volume*) | Root/data disks |
| **Instance Store** | Block | Ephemeral | No | Cache, buffers, temp data |
| **EFS** | File (NFS) | Persistent | Yes (many instances, multi-AZ) | Shared web assets, CMS |

\* *EBS Multi-Attach is the exception — see [EBS Multi-Attach](4-ebs-multi-attach.md).*
