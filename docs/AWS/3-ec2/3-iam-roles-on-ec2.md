# EC2 – Phase 3: IAM Roles on EC2 (CORE CONCEPT)

## Details (Teaching / Conceptual Understanding)

### What are IAM Roles for EC2?

IAM roles provide secure, temporary credentials to EC2 instances without storing access keys on the instance.

**Key insight:**
> EC2 instances **do not use IAM users or access keys**.  
> They assume **IAM Roles**.

**Why roles instead of access keys?**
- No credentials to manage or rotate
- Temporary credentials auto-rotate
- Secure by default
- AWS SDK/CLI automatically discovers credentials via IMDS

### IAM Role vs Instance Profile

**IAM Role:**
- Defines permissions (what the instance can do)
- Defines trust policy (which service can assume it)
- Can be assumed by multiple instances

**Instance Profile:**
- Container for **one IAM role**
- What EC2 actually attaches to an instance
- Links the role to the EC2 instance

> 📌 EC2 attaches **instance profiles**, not roles directly.  
> When you attach a role in the console, AWS automatically creates an instance profile behind the scenes.

### Required IAM Permissions (Important)

To attach a role to an EC2 instance, the **user** (not the instance) needs:

- `iam:ListInstanceProfiles` - to list available instance profiles
- `iam:PassRole` - to allow passing the role to EC2 service

**Why these permissions?**
- Security: Prevents unauthorized role assumption
- Compliance: Controls which roles can be attached
- Best practice: Principle of least privilege

**Note:** `PowerUserAccess` alone is **not sufficient**. These IAM permissions must be explicitly granted.

### Custom Policy Example

For developers who need to attach roles to EC2:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:ListInstanceProfiles",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

**Policy name:** `EC2AttachInstanceProfile`  
**Attached to:** `developers` group

### EC2 Metadata Service (IMDS)

The EC2 Instance Metadata Service provides information about the instance, including IAM role credentials.

**Metadata Endpoint:**
- IP: `169.254.169.254` (link-local address)
- Only accessible from **within** the EC2 instance
- Cannot be accessed from outside

**Why link-local?**
- No public routing
- Only accessible from the instance itself
- Secure by default

### IMDSv2 (Instance Metadata Service Version 2)

IMDSv2 uses token-based authentication to prevent SSRF (Server-Side Request Forgery) attacks.

**How it works:**

1. **Get a session token:**
```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
```

2. **Use token to query metadata:**
```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/
```

**Token parameters:**
- `ttl-seconds`: Token lifetime (e.g., 21600 = 6 hours)
- Token required for all metadata queries in IMDSv2

> 📌 Amazon Linux 2023 uses IMDSv2 by default for security.

### Verifying IAM Role Attachment

Once a role is attached to an EC2 instance, verify it from inside the instance:

#### Step 1: Get Metadata Token

```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
```

#### Step 2: Query IAM Credentials Endpoint

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Expected output:**
```
ec2-s3-access-role
```

**What this confirms:**
- ✅ Role is attached
- ✅ Instance profile is working
- ✅ Temporary credentials are available
- ✅ AWS SDK/CLI can auto-discover credentials

#### Step 3: Get Temporary Credentials (Optional)

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/ec2-s3-access-role
```

This returns temporary AWS credentials that can be used by AWS SDK/CLI.

### Using IAM Role Credentials

**AWS SDK/CLI automatically discovers credentials:**

Once a role is attached, the AWS CLI and SDKs automatically:
1. Query IMDS for temporary credentials
2. Use those credentials for API calls
3. Refresh credentials when they expire

**No configuration needed!**

```bash
# This works automatically without any credentials file
aws s3 ls
```

The AWS CLI automatically:
- Queries IMDS for credentials
- Uses the role's permissions
- Refreshes credentials as needed

### Example: EC2 Instance with S3 Access Role

**Role name:** `ec2-s3-access-role`

**Permissions:**
- `AmazonS3FullAccess` (managed policy)

**Trust policy:**
```json
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
```

This allows the EC2 service to assume this role.

**Attached to:** EC2 instance via instance profile

### Benefits of IAM Roles

**Security:**
- No access keys stored on instances
- Credentials automatically rotate
- No key management overhead

**Convenience:**
- AWS SDK/CLI auto-discovery
- No manual credential configuration
- Works immediately after role attachment

**Best Practice:**
- Use roles for all EC2 instances
- Never embed access keys in applications
- Follow principle of least privilege

## Step-by-Step Process

### 1. Create IAM Role

From AWS Console:
- `IAM` → `Roles` → `Create role`
- Select trusted entity: `AWS service` → `EC2`
- Attach policies (e.g., `AmazonS3FullAccess`)
- Name the role (e.g., `ec2-s3-access-role`)

### 2. Attach Role to EC2 Instance

From AWS Console:
- `EC2` → `Instances` → Select instance
- `Actions` → `Security` → `Modify IAM role`
- Select the role → `Update IAM role`

**Required permissions:** User must have `iam:PassRole` permission.

### 3. Verify Role Attachment (Inside Instance)

```bash
# Get metadata token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Check role name
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Test AWS CLI (auto-discovers credentials)
aws s3 ls
```

## AWS Console Navigation Paths

### Create IAM Role
`IAM` → `Roles` → `Create role` → `AWS service` → `EC2`

### Attach Role to Instance
`EC2` → `Instances` → Select instance → `Actions` → `Security` → `Modify IAM role`

### View Instance Profile
`IAM` → `Roles` → Select role → `Trust relationships` tab

### Check User Permissions
`IAM` → `Users` → Select user → `Permissions` tab

## FAQs & Interview / Certification Q&A

**Q: How do EC2 instances authenticate to AWS services?**
A: EC2 instances use IAM roles, not access keys. Credentials are provided via the Instance Metadata Service (IMDS).

**Q: What is the difference between an IAM role and an instance profile?**
A: An IAM role defines permissions and trust policy. An instance profile is a container for one IAM role that EC2 actually attaches to instances.

**Q: Can you attach multiple IAM roles to one EC2 instance?**
A: No, an EC2 instance can only have one instance profile (containing one IAM role) attached at a time.

**Q: What permissions does a user need to attach a role to EC2?**
A: The user needs `iam:ListInstanceProfiles` and `iam:PassRole` permissions. PowerUserAccess alone is not sufficient.

**Q: What is IMDSv2?**
A: Instance Metadata Service Version 2, which requires token-based authentication to prevent SSRF attacks.

**Q: How do you query IAM role credentials from an EC2 instance?**
A: Use IMDS endpoint: `http://169.254.169.254/latest/meta-data/iam/security-credentials/` with IMDSv2 token authentication.

**Q: Do you need to configure AWS credentials on an EC2 instance with an IAM role?**
A: No, AWS SDK and CLI automatically discover and use credentials from IMDS when a role is attached.

**Q: What IP address is used for the EC2 metadata service?**
A: `169.254.169.254` (link-local address), which is only accessible from within the EC2 instance.

**Q: Why should you use IAM roles instead of access keys on EC2?**
A: Roles provide temporary credentials that auto-rotate, require no manual management, and are more secure than storing access keys.

**Q: Can you access EC2 metadata service from outside the instance?**
A: No, the metadata service (169.254.169.254) is only accessible from within the EC2 instance itself.

## Current Status Checkpoint ✅

You have successfully:
- Understood the difference between IAM roles and instance profiles
- Learned how EC2 instances authenticate using roles
- Configured IAM permissions to attach roles
- Attached an IAM role to an EC2 instance
- Verified role attachment via IMDS
- Tested automatic credential discovery with AWS CLI

You are now ready to:
👉 Use AWS services from EC2 instances without credentials
👉 Implement secure application architectures
👉 Understand service-to-service authentication

### 🔒 Security Reminder
- **Never** embed access keys in EC2 instances
- Always use IAM roles for EC2 authentication
- Ensure users have `iam:PassRole` permission before attaching roles
- Use IMDSv2 for enhanced security
- Follow principle of least privilege for role permissions

### 💰 Cost Safety Reminder
Always stop or terminate EC2 instances when not actively learning:
- `EC2` → `Instances` → Select instance → `Instance state` → `Stop` or `Terminate`
