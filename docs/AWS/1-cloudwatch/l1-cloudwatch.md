# AWS CloudWatch Logs

## Navigation Path
**AWS Console → CloudWatch → Logs** (or search "CloudWatch Logs")

---

## Core Concepts

### What is CloudWatch Logs?
Managed service for collecting, storing, and querying logs from applications and AWS infrastructure.

**Key characteristics:**
- Centralizes logs (no log servers to manage)
- Used for debugging, monitoring, and audits
- Pay-per-use pricing model

### Log Groups vs Log Streams

**Log Group**: Logical container for related logs
- Represents: one application, service, or resource type
- Example: `/aws/lambda/payment-service`

**Log Stream**: Sequence of log events from a single source
- Usually one per: EC2 instance, container, Lambda execution
- Example: logs from a specific EC2 instance

**Relationship:**
```
Log Group (/aws/ec2/app)
 ├── Log Stream (instance-1)
 ├── Log Stream (instance-2)
 └── Log Stream (instance-3)
```

### How Logs Reach CloudWatch

Applications don't log directly to CloudWatch.

**Flow:**
```
Application → stdout/log file → Agent/Driver → CloudWatch Logs
```

**Common mechanisms:**
- **EC2**: CloudWatch Agent
- **ECS/EKS**: AWS log drivers / Fluent Bit
- **Lambda**: Automatic integration

---

## Limits & Costs

**Charges for:**
- Log ingestion (per GB)
- Log storage (per GB/month)
- Log queries (Log Insights)

**Key implication:** Excessive logging = higher AWS bill

**Best practices:**
- Use appropriate log levels
- Set retention policies
- Filter unnecessary logs

---

## Sample Code

### Send Logs from Python Application

```python
import boto3
import logging
from watchtower import CloudWatchLogHandler

# Configure CloudWatch handler
logger = logging.getLogger('myapp')
handler = CloudWatchLogHandler(
    log_group='/aws/myapp',
    stream_name='app-logs'
)
logger.addHandler(handler)

# Log messages
logger.info("Application started")
logger.error("Error occurred")
```

### Query Logs with Log Insights

```python
import boto3

logs_client = boto3.client('logs')

# Query logs
response = logs_client.start_query(
    logGroupName='/aws/lambda/my-function',
    startTime=int((datetime.now() - timedelta(hours=1)).timestamp()),
    endTime=int(datetime.now().timestamp()),
    queryString='fields @timestamp, @message | filter @message like /ERROR/'
)

query_id = response['queryId']

# Get results
results = logs_client.get_query_results(queryId=query_id)
```

### Create Log Group (AWS CLI)

```bash
aws logs create-log-group --log-group-name /aws/myapp

# Set retention (days)
aws logs put-retention-policy \
    --log-group-name /aws/myapp \
    --retention-in-days 7
```

---

## Interview Questions

**Q1: What is the difference between a Log Group and a Log Stream?**
- **Log Group**: Container for related logs (e.g., all logs from an application)
- **Log Stream**: Individual sequence of events from a single source (e.g., one EC2 instance)

**Q2: How do applications send logs to CloudWatch?**
- Applications don't send directly. They write to stdout/log files, which are collected by agents (CloudWatch Agent, Fluent Bit) or log drivers (ECS/EKS) that forward to CloudWatch.

**Q3: What are the costs associated with CloudWatch Logs?**
- Ingestion costs (per GB ingested), storage costs (per GB/month), and query costs (Log Insights queries).

**Q4: How do you reduce CloudWatch Logs costs?**
- Set appropriate retention policies, use log levels to filter unnecessary logs, aggregate logs where possible, and use log sampling for high-volume logs.

**Q5: What is CloudWatch Log Insights?**
- Interactive query tool to search and analyze log data using a query language. Useful for troubleshooting and analysis.

**Q6: How do you query logs in CloudWatch?**
- Use CloudWatch Log Insights with query syntax like: `fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc`

**Q7: What is the maximum log event size?**
- 256 KB per log event.

**Q8: How do you set up log retention?**
- Use `put-retention-policy` API or console to set retention period (1 day to Never expire). Logs older than retention are automatically deleted.

**Q9: What is the difference between CloudWatch Logs and CloudWatch Metrics?**
- **Logs**: Store log events and text data
- **Metrics**: Store numeric time-series data (CPU, memory, etc.)

**Q10: How do Lambda functions send logs to CloudWatch?**
- Automatically via Lambda execution role. Logs go to `/aws/lambda/<function-name>` log group.

**Q11: What is a subscription filter?**
- Real-time processing of log events. Can send logs to Kinesis, Lambda, or Elasticsearch for further processing.

**Q12: How do you export CloudWatch Logs?**
- Use `create-export-task` to export logs to S3. Useful for long-term storage or analysis outside CloudWatch.

**Q13: What are metric filters?**
- Transform log data into CloudWatch metrics. Define patterns in logs that trigger metric increments.

**Q14: How do you monitor log ingestion rate?**
- Use CloudWatch metrics: `IncomingLogEvents`, `IncomingBytes`, `DeliveryErrors` for the log group.

**Q15: What happens when log ingestion exceeds limits?**
- AWS throttles ingestion. Use exponential backoff in applications. Monitor `ThrottledEvents` metric.

---

## Key Takeaways

- CloudWatch Logs centralizes log management
- Log Groups organize **what** logs are
- Log Streams represent **where** logs come from
- Logs reach CloudWatch via agents/platform integrations
- Costs and limits are important design considerations
