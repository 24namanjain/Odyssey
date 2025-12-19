# AWS IAM (Identity and Access Management)

## Navigation Path in AWS Console
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

**Policy Structure**:
- **Effect**: Allow or Deny
- **Action**: The action to perform (e.g., `s3:GetObject`)
- **Resource**: ARN of what the action is performed on

**Key Rules**:
- Policies are stateless
- Evaluates on a per-request basis
- Explicit Deny overrides Allow

**Example Policy**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}
```

---

## Identity-based vs Resource-based Policies

### Identity-based Policies
**Attached to**:
- Users
- Groups
- Roles

**Purpose**: "What this identity can do"

**Used by**:
- EC2 instances
- ECS tasks
- Lambda functions
- Human users (via users/groups)

**Example** (Attached to a role):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}
```

### Resource-based Policies
**Attached to**:
- S3 buckets
- SQS queues
- SNS topics
- Lambda functions

**Purpose**: "Who can access this resource"

**Example** (S3 bucket policy):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::123456789012:user/john"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}
```

---

## Trust Policy (Role Assumption)

### What is a Trust Policy?
A trust policy defines **WHO** is allowed to assume an IAM role. It does **NOT** define permissions.

**Example Trust Policy**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            }
        }
    ]
}
```

### Key Components

| Component | Value | Explanation |
|-----------|-------|-------------|
| **Version** | `"2012-10-17"` | Policy language version (almost always this) |
| **Effect** | `"Allow"` | Allows the principal to assume the role |
| **Action** | `"sts:AssumeRole"` | Critical action - enables role assumption |
| **Principal** | Service/Account/User | Defines who can assume the role |

### Common Principals

**AWS Services**:
```json
"Principal": {
    "Service": [
        "ec2.amazonaws.com",        // EC2 instances
        "ecs-tasks.amazonaws.com",  // ECS tasks
        "lambda.amazonaws.com"      // Lambda functions
    ]
}
```

**Cross-Account Access**:
```json
"Principal": {
    "AWS": "arn:aws:iam::123456789012:root"
}
```

**Specific Role**:
```json
"Principal": {
    "AWS": "arn:aws:iam::123456789012:role/SomeRole"
}
```

### Trust Policy vs Permission Policy

| Aspect | Trust Policy | Permission Policy |
|--------|--------------|-------------------|
| **Question** | Who can assume this role? | What can the role do? |
| **Uses** | Principal, sts:AssumeRole | Action, Resource |
| **Attached to** | Role itself | Role as permissions |
| **Purpose** | Controls access to role | Controls what role can do |

**Key Takeaway**: A trust policy controls **WHO** can assume a role, not **WHAT** the role can do.

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
Writes logs to CloudWatch / Accesses AWS APIs
```

**No access keys in code. Ever.**

---

## Sample Code Examples

### Creating an IAM Role with Trust Policy (AWS CLI)

```bash
# Create trust policy file
cat > trust-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

# Create role
aws iam create-role \
    --role-name EC2-S3-Access-Role \
    --assume-role-policy-document file://trust-policy.json

# Attach permission policy
aws iam attach-role-policy \
    --role-name EC2-S3-Access-Role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile
aws iam create-instance-profile \
    --instance-profile-name EC2-S3-Access-Profile

# Add role to instance profile
aws iam add-role-to-instance-profile \
    --instance-profile-name EC2-S3-Access-Profile \
    --role-name EC2-S3-Access-Role
```

### Using IAM Role in EC2 (Python)

```python
import boto3

# No credentials needed - uses instance role automatically
s3_client = boto3.client('s3')

# List buckets
response = s3_client.list_buckets()
for bucket in response['Buckets']:
    print(f"Bucket: {bucket['Name']}")
```

### Assuming a Role (Cross-Account)

```python
import boto3

# Assume role in another account
sts_client = boto3.client('sts')

response = sts_client.assume_role(
    RoleArn='arn:aws:iam::123456789012:role/CrossAccountRole',
    RoleSessionName='MySession'
)

# Use temporary credentials
credentials = response['Credentials']
s3_client = boto3.client(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
```

### Creating a User with Programmatic Access

```bash
# Create user
aws iam create-user --user-name developer

# Create access key
aws iam create-access-key --user-name developer

# Attach policy
aws iam attach-user-policy \
    --user-name developer \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

---

## Interview Questions

### Basic Concepts

**Q1: What is the difference between IAM users and IAM roles?**
- **Users**: Permanent identities for humans or applications that need long-term credentials
- **Roles**: Temporary identities that can be assumed by users, services, or applications. No long-term credentials.

**Q2: What is the difference between a trust policy and a permission policy?**
- **Trust Policy**: Defines WHO can assume a role (uses Principal and sts:AssumeRole)
- **Permission Policy**: Defines WHAT actions can be performed (uses Action and Resource)

**Q3: What happens when both Allow and Deny are present in a policy?**
- Explicit Deny always overrides Allow. This is a fundamental rule in IAM policy evaluation.

**Q4: What is the difference between identity-based and resource-based policies?**
- **Identity-based**: Attached to users, groups, or roles. Defines what the identity can do.
- **Resource-based**: Attached to resources (S3, SQS, etc.). Defines who can access the resource.

### Policy Evaluation

**Q5: How does AWS evaluate IAM policies?**
1. Check for explicit Deny (if found, deny immediately)
2. Check for Allow (if found, allow)
3. Default deny (if no explicit allow)

**Q6: What is the principle of least privilege?**
- Grant only the minimum permissions necessary for a user/role to perform their tasks. This reduces security risk.

### Roles and Trust

**Q7: How do EC2 instances get credentials to access AWS services?**
- EC2 instances use IAM roles attached via instance profiles. The instance automatically retrieves temporary credentials from STS using the role's trust policy.

**Q8: Can a Lambda function assume an IAM role?**
- Lambda functions don't "assume" roles in the traditional sense. You attach an execution role to the Lambda, and AWS automatically provides temporary credentials.

**Q9: What is the difference between sts:AssumeRole and sts:AssumeRoleWithWebIdentity?**
- **AssumeRole**: For programmatic access, typically used by AWS services or cross-account access
- **AssumeRoleWithWebIdentity**: For web identity federation (OIDC, OAuth providers like Google, Facebook)

### Security Best Practices

**Q10: Why should you avoid using root account credentials?**
- Root account has full access to everything. If compromised, entire account is at risk. Always use IAM users/roles with least privilege.

**Q11: What is MFA and why is it important?**
- Multi-Factor Authentication adds an extra layer of security. Even if credentials are stolen, attacker needs the MFA device.

**Q12: How do you enable MFA for a user?**
- IAM → Users → Select user → Security credentials → Assign MFA device → Follow setup instructions

### Advanced Scenarios

**Q13: How do you grant cross-account access to S3?**
- Two approaches:
  1. Resource-based policy on S3 bucket allowing the other account
  2. Identity-based policy on a role in the other account, with trust policy allowing assumption

**Q14: What is IAM Access Analyzer?**
- Service that helps identify resources shared with external entities. Helps ensure least privilege and identify security risks.

**Q15: What is the difference between IAM policies and SCPs (Service Control Policies)?**
- **IAM Policies**: Applied to users, groups, roles within an account
- **SCPs**: Applied at the organization level, set maximum permissions for accounts in an OU

**Q16: Can you attach multiple policies to a role?**
- Yes, you can attach multiple managed policies and inline policies. The effective permissions are the union of all policies (unless there's an explicit deny).

**Q17: What happens when you delete an IAM user?**
- The user is deleted, but resources created by that user remain. You can optionally delete access keys, MFA devices, and other associated resources.

**Q18: What is the difference between managed policies and inline policies?**
- **Managed Policies**: Reusable, versioned, can be attached to multiple entities
- **Inline Policies**: Embedded directly in a user/role/group, deleted when entity is deleted

**Q19: How do you troubleshoot "Access Denied" errors?**
1. Check if policy has correct Effect (Allow)
2. Verify Action matches the API call
3. Verify Resource ARN is correct
4. Check for explicit Deny in other policies
5. Verify trust policy if using roles
6. Check SCPs if in an organization

**Q20: What is the maximum size of an IAM policy?**
- Managed policy: 6,144 characters
- Inline policy: 2,048 characters
- User can have up to 10 managed policies and 2 inline policies

---

## Best Practices

1. **Never use root account** for daily operations
2. **Enable MFA** for privileged users
3. **Use roles** instead of access keys when possible
4. **Follow least privilege** principle
5. **Use IAM Access Analyzer** to identify over-permissions
6. **Regularly rotate** access keys
7. **Use policy conditions** to restrict access (IP, time, etc.)
8. **Enable CloudTrail** to audit IAM actions
9. **Use managed policies** when possible for consistency
10. **Review and remove** unused IAM entities regularly

---

## Common Policy Conditions

```json
{
    "Condition": {
        "IpAddress": {
            "aws:SourceIp": "203.0.113.0/24"
        },
        "DateGreaterThan": {
            "aws:CurrentTime": "2024-01-01T00:00:00Z"
        },
        "StringEquals": {
            "aws:RequestedRegion": "us-east-1"
        }
    }
}
```

---

## Quick Reference

| Concept | Description |
|---------|-------------|
| **User** | Permanent identity with credentials |
| **Group** | Collection of users for easier policy management |
| **Role** | Temporary identity that can be assumed |
| **Policy** | Document defining permissions |
| **Trust Policy** | Defines who can assume a role |
| **Permission Policy** | Defines what actions are allowed |
| **STS** | Security Token Service - provides temporary credentials |
| **Instance Profile** | Container for IAM role when used with EC2 |
