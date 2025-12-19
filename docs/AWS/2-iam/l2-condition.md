# AWS IAM Conditions

## Navigation Path
**AWS Console → IAM → Policies → Create Policy → JSON → Add Condition**

---

## Core Concepts

### What are IAM Conditions?
Optional blocks inside IAM policy statements that add context-based restrictions to permissions.

**Purpose**: Answer "Under what circumstances is this action allowed or denied?"

**Key points:**
- Evaluated at request time
- Further limit an Allow or enforce a conditional Deny
- Conditions refine permissions, they don't replace scoping

### Policy Evaluation with Conditions

```
Explicit Deny → always wins
Explicit Allow → only if conditions are met
Default → deny
```

---

## Condition Structure

```json
"Condition": {
    "ConditionOperator": {
        "ConditionKey": "ConditionValue"
    }
}
```

- **Operator**: How comparison is done (StringEquals, IpAddress, etc.)
- **Key**: Request context attribute (aws:SourceIp, aws:CurrentTime, etc.)
- **Value**: Expected condition value

---

## Common Condition Categories

### IP-based Conditions (WHERE)

Restrict actions by source IP address.

**Example:**
```json
{
    "Effect": "Allow",
    "Action": "s3:*",
    "Resource": "*",
    "Condition": {
        "IpAddress": {
            "aws:SourceIp": "203.0.113.0/24"
        }
    }
}
```

**Use cases:**
- Admin access from office network
- Block unknown locations
- Restrict API access to specific IPs

### Time-based Conditions (WHEN)

Restrict actions to specific time windows.

**Example:**
```json
{
    "Effect": "Allow",
    "Action": "ec2:*",
    "Resource": "*",
    "Condition": {
        "DateGreaterThan": {
            "aws:CurrentTime": "2025-01-01T09:00:00Z"
        },
        "DateLessThan": {
            "aws:CurrentTime": "2025-01-01T17:00:00Z"
        }
    }
}
```

**Use cases:**
- Human access during business hours
- Prevent accidental off-hours changes
- Scheduled maintenance windows

### MFA-based Conditions (HOW)

Require MFA for sensitive actions.

**Example:**
```json
{
    "Effect": "Allow",
    "Action": "s3:DeleteBucket",
    "Resource": "*",
    "Condition": {
        "Bool": {
            "aws:MultiFactorAuthPresent": "true"
        }
    }
}
```

**Use cases:**
- Deleting resources
- Modifying IAM or billing
- Critical infrastructure changes

### Resource Tag Conditions (WHAT)

Restrict access based on resource tags.

**Example:**
```json
{
    "Effect": "Allow",
    "Action": "*",
    "Resource": "*",
    "Condition": {
        "StringEquals": {
            "aws:ResourceTag/environment": "dev"
        }
    }
}
```

**Use cases:**
- Environment isolation (dev vs prod)
- Team-based access control
- Cost center restrictions

---

## Common Condition Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `StringEquals` | Exact match | `"aws:ResourceTag/environment": "prod"` |
| `StringLike` | Wildcard matching | `"aws:ResourceTag/team": "dev-*"` |
| `Bool` | true/false checks | `"aws:MultiFactorAuthPresent": "true"` |
| `IpAddress` | IP range validation | `"aws:SourceIp": "203.0.113.0/24"` |
| `DateGreaterThan` | Time-based access | `"aws:CurrentTime": "2025-01-01T09:00:00Z"` |
| `DateLessThan` | Time-based access | `"aws:CurrentTime": "2025-01-01T17:00:00Z"` |

---

## Example Policies

### CloudWatch Logs with Tag Condition

Allow log writes only to prod resources.

```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "logs:PutLogEvents",
        "Resource": "*",
        "Condition": {
            "StringEquals": {
                "aws:ResourceTag/environment": "prod"
            }
        }
    }]
}
```

**Prevents:**
- Dev logs polluting prod
- Cross-environment mistakes

### Explicit Deny with MFA Condition

Deny all actions if MFA is not present.

```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Deny",
        "Action": "*",
        "Resource": "*",
        "Condition": {
            "Bool": {
                "aws:MultiFactorAuthPresent": "false"
            }
        }
    }]
}
```

**Meaning:**
- Deny all actions if MFA is not present
- Explicit deny overrides all allows
- Used in security-conscious organizations

### Multiple Conditions

Combine multiple conditions with AND logic.

```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "s3:DeleteObject",
        "Resource": "*",
        "Condition": {
            "Bool": {
                "aws:MultiFactorAuthPresent": "true"
            },
            "IpAddress": {
                "aws:SourceIp": "203.0.113.0/24"
            },
            "StringEquals": {
                "aws:ResourceTag/environment": "prod"
            }
        }
    }]
}
```

**All conditions must be true** for the policy to allow the action.

---

## Sample Code

### Create Policy with Condition (AWS CLI)

```bash
cat > policy-with-condition.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::my-bucket/*",
        "Condition": {
            "IpAddress": {
                "aws:SourceIp": "203.0.113.0/24"
            }
        }
    }]
}
EOF

aws iam create-policy \
    --policy-name S3-IP-Restricted \
    --policy-document file://policy-with-condition.json
```

### Test Condition Evaluation (Python)

```python
import boto3
from botocore.exceptions import ClientError

# This will work if source IP matches condition
try:
    s3_client = boto3.client('s3')
    response = s3_client.get_object(
        Bucket='my-bucket',
        Key='file.txt'
    )
    print("Access granted")
except ClientError as e:
    if e.response['Error']['Code'] == 'AccessDenied':
        print("Access denied - condition not met")
```

---

## Common Mistakes to Avoid

1. **Using conditions instead of proper resource scoping**
   - Conditions add restrictions, but should still scope resources properly

2. **Over-stacking multiple conditions unnecessarily**
   - Keep conditions simple and focused

3. **Forgetting conditions are evaluated at runtime**
   - Conditions check request context, not static values

4. **Applying conditions without understanding request context**
   - Know which condition keys are available for each service

5. **Using wrong condition operators**
   - Use StringEquals for exact match, StringLike for wildcards

---

## Interview Questions

**Q1: What are IAM conditions?**
- Optional blocks in policy statements that add context-based restrictions. They answer "under what circumstances" an action is allowed.

**Q2: When are conditions evaluated?**
- At request time, not when the policy is created. They check the context of each API request.

**Q3: What is the difference between StringEquals and StringLike?**
- **StringEquals**: Exact match
- **StringLike**: Wildcard matching (supports * and ?)

**Q4: How do you require MFA for sensitive actions?**
- Use condition: `"Bool": {"aws:MultiFactorAuthPresent": "true"}`

**Q5: Can you combine multiple conditions?**
- Yes, multiple conditions in the same Condition block use AND logic (all must be true).

**Q6: What happens if a condition is not met?**
- The policy statement is not applied. If it's an Allow statement, the action is denied (default deny).

**Q7: How do you restrict access by IP address?**
- Use condition: `"IpAddress": {"aws:SourceIp": "203.0.113.0/24"}`

**Q8: What is the difference between aws:ResourceTag and aws:RequestTag?**
- **aws:ResourceTag**: Checks tags on the resource being accessed
- **aws:RequestTag**: Checks tags in the request (for create/update operations)

**Q9: How do you restrict access to specific time windows?**
- Use DateGreaterThan and DateLessThan conditions with aws:CurrentTime.

**Q10: Can conditions be used with Deny statements?**
- Yes, explicit Deny with conditions is a powerful pattern for safety nets (e.g., deny all if MFA not present).

**Q11: What condition keys are available?**
- Service-specific keys (e.g., s3:VersionId) and global keys (e.g., aws:SourceIp, aws:CurrentTime, aws:MultiFactorAuthPresent).

**Q12: How do you enforce environment isolation using conditions?**
- Use resource tag conditions: `"StringEquals": {"aws:ResourceTag/environment": "dev"}`

**Q13: What is the precedence when multiple policies have conditions?**
- Explicit Deny always wins. Then Allow statements are evaluated, and all conditions must be met.

**Q14: Can you use conditions with resource-based policies?**
- Yes, conditions work with both identity-based and resource-based policies.

**Q15: How do you test if a condition is working correctly?**
- Use IAM Policy Simulator in AWS Console, or make actual API calls and check for AccessDenied errors.

---

## Key Takeaways

- Conditions add precision, not power
- Best used to enforce least privilege
- Explicit deny + conditions are powerful safety nets
- Senior AWS usage relies heavily on conditions
- Conditions make permissions context-aware by restricting when, where, and how actions are allowed

---

## Quick Reference

| Condition Type | Key | Operator | Use Case |
|----------------|-----|----------|----------|
| IP-based | `aws:SourceIp` | `IpAddress` | Restrict by location |
| Time-based | `aws:CurrentTime` | `DateGreaterThan/LessThan` | Business hours |
| MFA | `aws:MultiFactorAuthPresent` | `Bool` | Require MFA |
| Resource Tag | `aws:ResourceTag/*` | `StringEquals` | Environment isolation |
| Request Tag | `aws:RequestTag/*` | `StringEquals` | Tag enforcement |
