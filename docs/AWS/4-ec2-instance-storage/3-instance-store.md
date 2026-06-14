---
title: EC2 Instance Store
tags: [aws, ec2, instance-store, storage, ephemeral]
---

# EC2 Instance Store

## Console paths

> **Instance types with local NVMe:** `AWS Console` › `EC2` › `Instance types` › filter by *Instance storage*

> **View attached instance store:** `AWS Console` › `EC2` › `Instances` › select instance › `Storage` tab

---

## What is Instance Store?

**Instance Store** (also called **ephemeral storage**) is **physical disk attached directly to the host** running your EC2 instance.

Unlike EBS:
- It is **not** a separate network volume
- It offers **very high IOPS** and low latency
- Data is **not durable** — it is lost when the instance is stopped or terminated (depending on event type)

Think of it as a **high-speed scratch disk**, not long-term storage.

---

## When to use it

| Good for | Bad for |
|----------|---------|
| Buffers | Databases (primary storage) |
| Caches | Anything that must survive reboot |
| Temporary scratch space | User uploads you cannot lose |
| High-throughput temp processing | Compliance/regulated data retention |

---

## Instance Store vs EBS

| | Instance Store | EBS |
|---|----------------|-----|
| **Location** | Local to physical host | Network-attached |
| **Performance** | Very high IOPS | High (depends on type) |
| **Durability** | Ephemeral | Persistent |
| **Survives stop?** | ❌ No (data lost) | ✅ Yes |
| **Resize** | Fixed at launch | Can modify volume size |

> 📌 Some instance families (e.g. `i3`, `c5d`, `m5d`) include NVMe instance store volumes. Check the instance type details before launch.

---

## FAQs

**Q: Can I add instance store after launch?**
No. Instance store is tied to the instance type selected at launch.

**Q: Is instance store free?**
You pay for the instance type — the local storage is included in that price, not billed separately like EBS.

**Q: What happens on stop vs terminate?**
For most instance store volumes, data is **lost on stop and terminate**. Always confirm behavior for your specific instance type in AWS docs.
