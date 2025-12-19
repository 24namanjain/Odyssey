# AWS IAM Policies - Practice Examples

## Navigation Path
**AWS Console → IAM → Policies → Create Policy**

---

## Policy 1: EC2 CloudWatch Logs (Least Privilege)

### Use Case
Backend service running on EC2 needs to write logs to CloudWatch.

### Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ],
        "Resource": "*"
    }]
}
```

### Why This Exists
- Enables logging functionality
- Nothing else (no read, no delete)
- Minimum required actions for log writing

### Real-world Note
In production, scope the resource ARN:
```json
"Resource": [
    "arn:aws:logs:us-east-1:123456789012:log-group:/aws/ec2/app:*"
]
```

Wildcard is acceptable when:
- Log group is created dynamically
- App is early-stage
- Multiple log groups needed

---

## Policy 2: Developers - DEV Resources Only (Tag-based)

### Use Case
Developers should never touch prod resources. Enforce environment isolation.

### Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "*",
        "Resource": "*",
        "Condition": {
            "StringEquals": {
                "aws:ResourceTag/environment": "dev"
            }
        }
    }]
}
```

### Why This Exists
- Enforces environment isolation
- Prevents "oops, I modified prod" mistakes
- Extremely common in mature AWS setups

### Key Insight
Tags become part of your security model, not just metadata.

### Enhanced Version (More Secure)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:*",
                "s3:*",
                "rds:*"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/environment": "dev"
                }
            }
        },
        {
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "StringNotEquals": {
                    "aws:ResourceTag/environment": "dev"
                }
            }
        }
    ]
}
```

---

## Policy 3: MFA Required (Safety Net)

### Use Case
Protect sensitive AWS accounts from accidental or malicious actions.

### Policy
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

### Why This Exists
- Forces MFA for everything
- Explicit deny overrides all allows
- Used in security-conscious organizations

### Important
This is usually applied:
- To human users
- At account or org level
- **Not** typically for services (EC2, Lambda, etc.)

### When to Use
- Production accounts
- Accounts with sensitive data
- Compliance requirements
- Shared accounts

---

## Policy 4: S3 Bucket Access with IP Restriction

### Use Case
Allow S3 access only from office network.

### Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:ListBucket"
        ],
        "Resource": [
            "arn:aws:s3:::my-bucket",
            "arn:aws:s3:::my-bucket/*"
        ],
        "Condition": {
            "IpAddress": {
                "aws:SourceIp": "203.0.113.0/24"
            }
        }
    }]
}
```

---

## Policy 5: Time-based Access Control

### Use Case
Restrict access to business hours only.

### Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "ec2:*",
        "Resource": "*",
        "Condition": {
            "DateGreaterThan": {
                "aws:CurrentTime": "09:00Z"
            },
            "DateLessThan": {
                "aws:CurrentTime": "17:00Z"
            },
            "StringEquals": {
                "aws:RequestedRegion": "us-east-1"
            }
        }
    }]
}
```

---

## Sample Code

### Create and Attach Policy (AWS CLI)

```bash
# Create policy
cat > ec2-logs-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ],
        "Resource": "*"
    }]
}
EOF

aws iam create-policy \
    --policy-name EC2-CloudWatch-Logs \
    --policy-document file://ec2-logs-policy.json

# Attach to role
aws iam attach-role-policy \
    --role-name EC2-Role \
    --policy-arn arn:aws:iam::123456789012:policy/EC2-CloudWatch-Logs
```

### Create Tag-based Policy (Python)

```python
import boto3
import json

iam_client = boto3.client('iam')

policy_doc = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "*",
        "Resource": "*",
        "Condition": {
            "StringEquals": {
                "aws:ResourceTag/environment": "dev"
            }
        }
    }]
}

response = iam_client.create_policy(
    PolicyName='DevOnlyAccess',
    PolicyDocument=json.dumps(policy_doc)
)

print(f"Policy ARN: {response['Policy']['Arn']}")
```

---

## Mental Model: Policy Design

| Policy Type | Purpose | Pattern |
|-------------|---------|---------|
| **Policy 1** | Enable app functionality | Allow specific actions |
| **Policy 2** | Enforce environment boundaries | Condition-based restrictions |
| **Policy 3** | Prevent catastrophic mistakes | Explicit Deny with conditions |

### Good IAM Design Uses:
- **Allow** for capability
- **Conditions** for precision
- **Deny** for guardrails

### Common Beginner Mistake
**"One policy to rule them all"** - trying to do everything in one policy.

### Senior Engineer Approach
- Multiple small policies
- Clear intent per policy
- Explicit denies sparingly
- Conditions for fine-grained control

---

## Interview Questions

**Q1: What is the principle of least privilege in IAM?**
- Grant only the minimum permissions necessary. Policy 1 demonstrates this by allowing only log writing actions, nothing more.

**Q2: How do you prevent developers from accessing production resources?**
- Use tag-based conditions (Policy 2). Tag resources with environment tags and restrict access based on tags.

**Q3: What is the difference between using Action: "*" with conditions vs specific actions?**
- Action: "*" with conditions is broader but relies on conditions for security. Specific actions are more explicit and easier to audit.

**Q4: Why use explicit Deny with MFA condition?**
- Explicit Deny always overrides Allow. This ensures that even if other policies allow actions, MFA must be present (Policy 3).

**Q5: How do you scope a policy to specific resources?**
- Use Resource ARN instead of "*". Example: `"Resource": "arn:aws:s3:::my-bucket/*"`

**Q6: Can you combine multiple conditions in one policy?**
- Yes, multiple conditions in the Condition block use AND logic. All must be true for the policy to apply.

**Q7: What happens if a resource doesn't have the required tag?**
- The condition fails, and the policy doesn't apply. For tag-based restrictions, this means access is denied.

**Q8: How do you test if a policy works correctly?**
- Use IAM Policy Simulator in AWS Console, or make actual API calls and verify behavior.

**Q9: What is the difference between Resource: "*" and scoped resources?**
- "*" allows access to all resources (subject to conditions). Scoped resources limit to specific ARNs for better security.

**Q10: When should you use explicit Deny statements?**
- For safety nets (like MFA requirement), to override other policies, or to enforce mandatory restrictions.

**Q11: How do you handle dynamic resource creation with policies?**
- Use wildcards in Resource ARN or use conditions to match resource patterns. For logs, "*" is common since log groups are created dynamically.

**Q12: What is the best practice for policy size?**
- Keep policies small and focused. Multiple small policies are better than one large policy. Maximum size: 6,144 characters for managed policies.

**Q13: How do you enforce tagging requirements?**
- Use conditions like `aws:RequestTag` to require tags on creation, or use SCPs (Service Control Policies) at organization level.

**Q14: What is the difference between inline and managed policies?**
- **Managed**: Reusable, versioned, can be attached to multiple entities
- **Inline**: Embedded in entity, deleted when entity is deleted

**Q15: How do you audit policy effectiveness?**
- Use IAM Access Analyzer, CloudTrail logs, and IAM Policy Simulator. Review unused permissions regularly.

---

## Best Practices

1. **Start with least privilege** - Grant minimum required permissions
2. **Use conditions for precision** - Don't rely solely on Action/Resource scoping
3. **Tag resources consistently** - Tags enable condition-based access control
4. **Use explicit Deny sparingly** - Only for critical safety nets
5. **Test policies before deploying** - Use Policy Simulator
6. **Document policy purpose** - Add descriptions explaining why policies exist
7. **Review and audit regularly** - Remove unused permissions
8. **Use managed policies when possible** - Easier to maintain and version
9. **Combine policies strategically** - Multiple small policies > one large policy
10. **Monitor policy changes** - Use CloudTrail to track IAM modifications

---

## Quick Reference

| Policy Pattern | Use Case | Key Elements |
|----------------|----------|--------------|
| **Least Privilege** | Enable specific functionality | Specific Actions, Scoped Resources |
| **Tag-based** | Environment isolation | Condition: aws:ResourceTag |
| **MFA Required** | Security guardrail | Effect: Deny, Condition: MFA |
| **IP Restriction** | Network-based access | Condition: aws:SourceIp |
| **Time-based** | Business hours | Condition: aws:CurrentTime |
