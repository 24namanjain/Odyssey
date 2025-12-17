---
title: AWS CloudWatch Logs - Level 1
tags: [aws, cloudwatch, logging, monitoring, beginner]
---

# AWS CloudWatch Logs — Level 1

## What CloudWatch Logs is

AWS CloudWatch Logs is a managed AWS service for collecting, storing, and querying logs.

**Key characteristics:**

* Centralizes logs from applications and AWS infrastructure
* Removes the need to manage log servers or storage
* Primarily used for debugging, monitoring, and audits

**Think of it as:** AWS's built-in log backend

## Log Groups vs Log Streams

### Log Group

A logical container for related logs.

**Usually represents:**

* One application
* One service
* One AWS resource type

**Examples:**

```
/aws/ec2/account-service
/aws/lambda/payment-service
```

> 💡 **Comparable to:** A Loki job or label grouping

### Log Stream

A sequence of log events from a single source.

**Usually one per:**

* EC2 instance
* Container
* Lambda execution environment

> 💡 **Comparable to:** Logs from a single pod or container

### Relationship

```
Log Group
 ├── Log Stream (instance-1)
 ├── Log Stream (instance-2)
 └── Log Stream (instance-3)
```

## How Applications Send Logs to CloudWatch

Applications do **not** log directly to CloudWatch.

**Typical flow:**

```
Application
 → stdout / log file
   → agent / log driver
     → CloudWatch Logs
```

**Common mechanisms:**

* **EC2** → CloudWatch Agent
* **ECS / EKS** → AWS log drivers / Fluent Bit
* **Lambda** → automatic integration

**This is conceptually identical to:**

```
Spring Boot → Promtail → Loki
```

Different names, same architecture.

## Limits & Costs (High Level)

CloudWatch Logs is **not free**.

**You are charged for:**

* Log ingestion (per GB)
* Log storage (per GB per month)
* Log queries (Log Insights)

**There are:**

* Ingestion rate limits
* Retention limits
* Size limits per log event

**Key implication:** Excessive logging = higher AWS bill

This is why log levels, retention, and filtering matter in production.

## Key Takeaways

* CloudWatch Logs is a centralized, managed logging system
* Log Groups organize **what** the logs are
* Log Streams represent **where** logs come from
* Logs reach CloudWatch via agents or platform integrations
* Limits and costs are design constraints, not afterthoughts

## Mental Mapping (Important)

| Loki/Open Source | AWS CloudWatch |
|-----------------|----------------|
| Promtail | CloudWatch Agent |
| Loki | CloudWatch Logs |
| Grafana Explore | CloudWatch Log Insights |
| Loki 429 rate limit | CloudWatch ingestion limits & cost spikes |