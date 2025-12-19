# AWS IAM (Identity and Access Management)

## Navigation Path
**AWS Console → IAM** (or search "IAM" in services)

Key sections:
- **Users**: `IAM → Users`
- **Groups**: `IAM → User groups`
- **Roles**: `IAM → Roles`
- **Policies**: `IAM → Policies`
- **Access Analyzer**: `IAM → Access Analyzer`

---

## Core Concepts

### IAM Policy
**Question**: Can *THIS* identity perform *THIS* action on *THIS* resource?

**Structure:**
- **Effect**: Allow or Deny
- **Action**: The action to perform (e.g., `s3:GetObject`)
- **Resource**: ARN of what the action is performed on

**Key Rules:**
- Policies are stateless
- Evaluates on a per-request basis
- Explicit Deny overrides Allow

**Example:**
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::my-bucket/*"
    }]
}
```

---

## Identity-based vs Resource-based Policies

### Identity-based Policies
**Attached to**: Users, Groups, Roles  
**Purpose**: "What this identity can do"

**Used by**: EC2, ECS, Lambda, Human users

**Example:**
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Resource": "arn:aws:s3:::my-bucket/*"
    }]
}
```

### Resource-based Policies
**Attached to**: S3 buckets, SQS queues, SNS topics, Lambda functions  
**Purpose**: "Who can access this resource"

**Example (S3 bucket policy):**
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": "arn:aws:iam::123456789012:user/john"},
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::my-bucket/*"
    }]
}
```

---

## Trust Policy (Role Assumption)

### What is a Trust Policy?
Defines **WHO** can assume an IAM role. Does **NOT** define permissions.

**Example:**
```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Principal": {"Service": "ec2.amazonaws.com"}
    }]
}
```

### Key Components

| Component | Explanation |
|-----------|-------------|
| **Version** | Policy language version (`"2012-10-17"`) |
| **Effect** | Allow/Deny (usually Allow) |
| **Action** | `sts:AssumeRole` (critical for role assumption) |
| **Principal** | Who can assume the role (Service/Account/User) |

### Common Principals

**AWS Services:**
```json
"Principal": {
    "Service": [
        "ec2.amazonaws.com",
        "ecs-tasks.amazonaws.com",
        "lambda.amazonaws.com"
    ]
}
```

**Cross-Account:**
```json
"Principal": {"AWS": "arn:aws:iam::123456789012:root"}
```

### Trust Policy vs Permission Policy

| Aspect | Trust Policy | Permission Policy |
|--------|--------------|-------------------|
| **Question** | Who can assume this role? | What can the role do? |
| **Uses** | Principal, sts:AssumeRole | Action, Resource |
| **Attached to** | Role itself | Role as permissions |

**Key Takeaway**: Trust policy controls **WHO** can assume a role, not **WHAT** the role can do.

---

## Real-world Flow

```
EC2 Instance
    ↓
Assumes IAM Role (via Trust Policy)
    ↓
Gets Temporary Credentials (STS)
    ↓
Uses Permission Policy
    ↓
Accesses AWS APIs
```

**No access keys in code. Ever.**

---

## Sample Code

### Create IAM Role (AWS CLI)

```bash
# Create trust policy
cat > trust-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}
EOF

# Create role
aws iam create-role \
    --role-name EC2-S3-Role \
    --assume-role-policy-document file://trust-policy.json

# Attach permission policy
aws iam attach-role-policy \
    --role-name EC2-S3-Role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile
aws iam create-instance-profile \
    --instance-profile-name EC2-S3-Profile

aws iam add-role-to-instance-profile \
    --instance-profile-name EC2-S3-Profile \
    --role-name EC2-S3-Role
```

### Use IAM Role in EC2 (Python)

```python
import boto3

# No credentials needed - uses instance role automatically
s3_client = boto3.client('s3')
response = s3_client.list_buckets()
for bucket in response['Buckets']:
    print(f"Bucket: {bucket['Name']}")
```

### Assume Role (Cross-Account)

```python
import boto3

sts_client = boto3.client('sts')
response = sts_client.assume_role(
    RoleArn='arn:aws:iam::123456789012:role/CrossAccountRole',
    RoleSessionName='MySession'
)

credentials = response['Credentials']
s3_client = boto3.client(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
```

---

## Interview Questions

**Q1: What is the difference between IAM users and IAM roles?**
- **Users**: Permanent identities with long-term credentials
- **Roles**: Temporary identities that can be assumed. No long-term credentials.

**Q2: What is the difference between a trust policy and a permission policy?**
- **Trust Policy**: Defines WHO can assume a role (uses Principal and sts:AssumeRole)
- **Permission Policy**: Defines WHAT actions can be performed (uses Action and Resource)

**Q3: What happens when both Allow and Deny are present?**
- Explicit Deny always overrides Allow.

**Q4: What is the difference between identity-based and resource-based policies?**
- **Identity-based**: Attached to users/groups/roles. Defines what the identity can do.
- **Resource-based**: Attached to resources (S3, SQS, etc.). Defines who can access the resource.

**Q5: How does AWS evaluate IAM policies?**
1. Check for explicit Deny (if found, deny immediately)
2. Check for Allow (if found, allow)
3. Default deny (if no explicit allow)

**Q6: How do EC2 instances get credentials?**
- EC2 instances use IAM roles attached via instance profiles. The instance automatically retrieves temporary credentials from STS.

**Q7: Can a Lambda function assume an IAM role?**
- Lambda functions don't "assume" roles. You attach an execution role, and AWS automatically provides temporary credentials.

**Q8: What is the difference between sts:AssumeRole and sts:AssumeRoleWithWebIdentity?**
- **AssumeRole**: For programmatic access (AWS services, cross-account)
- **AssumeRoleWithWebIdentity**: For web identity federation (OIDC, OAuth)

**Q9: Why avoid root account credentials?**
- Root account has full access. If compromised, entire account is at risk. Use IAM users/roles with least privilege.

**Q10: How do you grant cross-account access to S3?**
- Two approaches:
  1. Resource-based policy on S3 bucket allowing the other account
  2. Identity-based policy on a role in the other account, with trust policy allowing assumption

**Q11: What is IAM Access Analyzer?**
- Service that identifies resources shared with external entities. Helps ensure least privilege.

**Q12: What is the difference between IAM policies and SCPs?**
- **IAM Policies**: Applied to users/groups/roles within an account
- **SCPs**: Applied at organization level, set maximum permissions for accounts in an OU

**Q13: Can you attach multiple policies to a role?**
- Yes. Effective permissions are the union of all policies (unless there's an explicit deny).

**Q14: What is the difference between managed and inline policies?**
- **Managed Policies**: Reusable, versioned, can be attached to multiple entities
- **Inline Policies**: Embedded directly in entity, deleted when entity is deleted

**Q15: How do you troubleshoot "Access Denied" errors?**
1. Check if policy has correct Effect (Allow)
2. Verify Action matches the API call
3. Verify Resource ARN is correct
4. Check for explicit Deny in other policies
5. Verify trust policy if using roles
6. Check SCPs if in an organization

---

## Best Practices

1. Never use root account for daily operations
2. Enable MFA for privileged users
3. Use roles instead of access keys when possible
4. Follow least privilege principle
5. Use IAM Access Analyzer to identify over-permissions
6. Regularly rotate access keys
7. Use policy conditions to restrict access (IP, time, etc.)
8. Enable CloudTrail to audit IAM actions
9. Use managed policies when possible
10. Review and remove unused IAM entities regularly

---

## Quick Reference

| Concept | Description |
|---------|-------------|
| **User** | Permanent identity with credentials |
| **Group** | Collection of users for policy management |
| **Role** | Temporary identity that can be assumed |
| **Policy** | Document defining permissions |
| **Trust Policy** | Defines who can assume a role |
| **Permission Policy** | Defines what actions are allowed |
| **STS** | Security Token Service - provides temporary credentials |
| **Instance Profile** | Container for IAM role when used with EC2 |
