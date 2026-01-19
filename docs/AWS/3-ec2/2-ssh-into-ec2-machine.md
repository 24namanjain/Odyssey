---
notion_page_id: 2edff901-fc97-81e8-a761-ddc89c0df95b
---

# EC2 – Phase 2: SSH into EC2 Instance

## Details (Teaching / Conceptual Understanding)

### What is SSH?

SSH (Secure Shell) is a protocol for secure remote access to a Linux/Unix machine.

**Key concepts:**
- Encrypted connection
- Key-based authentication (more secure than passwords)
- Terminal access to run commands
- Works on port 22

### Prerequisites for SSH

1. **Key pair file** (`.pem` file) downloaded from AWS
2. **Public IP address** of the EC2 instance
3. **Security group** allowing inbound SSH (port 22) from your IP
4. **Proper permissions** on the key file

### Setting Key File Permissions

```bash
chmod 400 aws-lab-key.pem
```

**Why is this necessary?**
- SSH requires restrictive permissions on private keys for security
- Without proper permissions, SSH will refuse to use the key
- `400` = read-only for owner (most restrictive safe option)

> 📌 SSH enforces this to prevent accidental key exposure.

### SSH Connection Command

```bash
ssh -i aws-lab-key.pem ec2-user@<PUBLIC_IP>
```

**Command breakdown:**
- `ssh` = SSH client command
- `-i aws-lab-key.pem` = specify identity file (your private key)
- `ec2-user@` = username for Amazon Linux
- `<PUBLIC_IP>` = public IP address of your EC2 instance

**Default usernames by OS:**
- Amazon Linux 2023: `ec2-user`
- Ubuntu: `ubuntu`
- RHEL: `ec2-user`
- CentOS: `centos`

### Host Key Verification

On first connection, SSH will prompt:

```
The authenticity of host '98.89.6.172 (98.89.6.172)' can't be established.
ED25519 key fingerprint is SHA256:UmOGmezpqcfsH9RXTXy9eUWadlabvH9CrlQbPNadfmA.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```

**What's happening:**
- SSH verifies the server's identity using a host key
- Prevents man-in-the-middle attacks
- On first connection, you verify and accept the fingerprint
- SSH saves it to `~/.ssh/known_hosts` for future connections

> 📌 Type `yes` to accept and continue. The fingerprint is unique to each server.

### Connection Refused Error

**Initial error encountered:**
```
ssh: connect to host 98.89.6.172 port 22: Connection refused
```

**Common causes:**
1. **Security group** blocking port 22 from your IP
2. **Instance not fully started** (wait 30-60 seconds after launch)
3. **SSH service not running** on the instance (rare with Amazon Linux)
4. **Network ACL** blocking traffic (advanced)

**Resolution:**
- Wait for instance to fully initialize
- Verify security group allows SSH from your IP
- Retry the connection

> 📌 Security groups are checked first, before the OS even sees the connection attempt.

### Verifying Connection

Once connected, verify basic information:

```bash
# Check current directory contents
ls

# Check current user
whoami

# Check OS version
cat /etc/os-release
```

**Expected output confirms:**
- You're logged in as `ec2-user`
- Instance is running Amazon Linux 2023
- You have shell access to the instance

### EC2 Instance Metadata Service

EC2 provides metadata about the instance at a special IP address.

**IMDSv2 (Instance Metadata Service Version 2):**

```bash
# Step 1: Get a session token (valid for specified TTL)
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Step 2: Use token to access metadata
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/
```

**Important points:**
- IP `169.254.169.254` is the metadata service endpoint
- Only accessible FROM within the instance
- IMDSv2 requires a token for security (prevents SSRF attacks)
- Token TTL can be set (21600 seconds = 6 hours in example)

**Why IMDSv2?**
- Prevents Server-Side Request Forgery (SSRF) attacks
- Token-based authentication adds security layer
- Amazon Linux 2023 uses IMDSv2 by default

### Metadata Endpoints

**Available metadata categories:**
- `ami-id` - AMI identifier
- `instance-id` - EC2 instance ID
- `instance-type` - Instance type (e.g., t2.micro)
- `local-ipv4` - Private IP address
- `public-ipv4` - Public IP address
- `security-groups` - Security group names
- `iam/security-credentials/` - IAM role credentials (if attached)

### IAM Role Access

**When no IAM role is attached:**

```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Returns:** 404 - Not Found

**Why:**
- No IAM role is attached to the instance
- Without a role, the instance has no AWS credentials
- The instance cannot access AWS services programmatically

> 📌 This is why IAM roles are important for EC2 instances to access AWS services securely.

### Network Connectivity Test

```bash
ping -c 2 google.com
```

**What this confirms:**
- Instance has internet connectivity
- Outbound traffic works (default security group allows it)
- DNS resolution works

**Output interpretation:**
- `64 bytes from...` = successful ping
- `time=1.87 ms` = round-trip time
- `0% packet loss` = all packets received
- Low latency indicates good connectivity

## Step-by-Step SSH Process

### 1. Locate Your Key File

```bash
cd ~/aws  # or wherever you saved the .pem file
ls        # verify the file exists
```

### 2. Set Proper Permissions

```bash
chmod 400 aws-lab-key.pem
```

### 3. Get Public IP Address

From AWS Console:
- `EC2` → `Instances` → Select your instance → Check `Public IPv4 address`

Or from terminal:
```bash
aws ec2 describe-instances --instance-ids i-xxxxx --query 'Reservations[0].Instances[0].PublicIpAddress'
```

### 4. Connect via SSH

```bash
ssh -i aws-lab-key.pem ec2-user@<PUBLIC_IP>
```

Replace `<PUBLIC_IP>` with your instance's actual public IP.

### 5. Accept Host Key (First Time Only)

Type `yes` when prompted to accept the host fingerprint.

### 6. Verify Connection

Once connected, verify you're on the instance:

```bash
whoami        # Should show: ec2-user
hostname      # Should show instance hostname
```

### 7. Test Metadata Access

```bash
# Get token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Query metadata
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id
```

### 8. Exit SSH Session

```bash
exit
```

Or press `Ctrl+D`

## Troubleshooting Common Issues

### Issue: "Permission denied (publickey)"

**Causes:**
- Wrong key file specified
- Key file permissions too open
- Wrong username for the AMI
- Key pair not associated with instance

**Solutions:**
1. Verify key file path: `ls -la aws-lab-key.pem`
2. Set permissions: `chmod 400 aws-lab-key.pem`
3. Check username (Amazon Linux 2023 = `ec2-user`)
4. Verify key pair name matches in AWS Console

### Issue: "Connection timed out"

**Causes:**
- Security group blocking SSH
- Network ACL blocking (advanced)
- Instance not running

**Solutions:**
1. Check security group allows SSH (port 22) from your IP
2. Verify instance state is "running"
3. Check your current IP hasn't changed

### Issue: "Connection refused"

**Causes:**
- Instance still initializing
- SSH service not running (rare)

**Solutions:**
1. Wait 30-60 seconds after launch
2. Verify instance passed status checks
3. Retry connection

### Issue: "Host key verification failed"

**Causes:**
- Host key changed (instance was recreated with same IP)
- Known hosts entry is stale

**Solution:**
```bash
ssh-keygen -R <PUBLIC_IP>  # Remove old entry
```

Then reconnect and accept new fingerprint.

## AWS Console Navigation Paths

### Get Public IP
`EC2` → `Instances` → Select instance → `Details` tab → `Public IPv4 address`

### Check Security Group
`EC2` → `Instances` → Select instance → `Security` tab → `Security groups`

### Verify Key Pair
`EC2` → `Instances` → Select instance → `Details` tab → `Key pair name`

### Check Instance State
`EC2` → `Instances` → `Instance state` column

## FAQs & Interview / Certification Q&A

**Q: What command do you use to SSH into an EC2 instance?**
A: `ssh -i <key-file>.pem ec2-user@<public-ip>` (for Amazon Linux)

**Q: Why do you need to set permissions on the .pem file?**
A: SSH enforces strict permissions on private keys for security. The key file must be readable only by the owner (typically `chmod 400`).

**Q: What is the default username for Amazon Linux 2023?**
A: `ec2-user`

**Q: What is the EC2 instance metadata service?**
A: A service accessible only from within an EC2 instance at `169.254.169.254` that provides information about the instance itself (instance ID, IP, security groups, IAM credentials, etc.).

**Q: What is IMDSv2?**
A: Instance Metadata Service Version 2, which requires a session token to access metadata, providing protection against SSRF attacks.

**Q: How do you access instance metadata with IMDSv2?**
A: First get a token using `PUT` request to `/latest/api/token`, then include the token in subsequent metadata requests using the `X-aws-ec2-metadata-token` header.

**Q: Why would you get a 404 when accessing IAM credentials metadata?**
A: No IAM role is attached to the instance. The instance needs an IAM role to have AWS credentials accessible via the metadata service.

**Q: What happens if you lose your .pem key file?**
A: You cannot SSH into the instance. AWS does not store or recover private keys. You would need to terminate the instance and launch a new one with a new key pair.

**Q: Can you SSH into an EC2 instance from anywhere?**
A: Only if the security group allows SSH (port 22) from your source IP address. Security groups control inbound access.

**Q: What port does SSH use?**
A: Port 22 (default)

**Q: How do you exit an SSH session?**
A: Type `exit` or press `Ctrl+D`

## Current Status Checkpoint ✅

You have successfully:
- Set proper permissions on the SSH key file
- Connected to EC2 instance via SSH
- Verified connection and OS information
- Accessed EC2 instance metadata service (IMDSv2)
- Understood the relationship between IAM roles and metadata service
- Tested network connectivity from the instance

You are now ready to:
👉 Configure IAM roles for EC2 (next phase)
👉 Run applications on the instance
👉 Understand EC2 instance storage and networking

### 🔒 Security Reminder
- Your SSH key is sensitive - keep it secure
- Never share your `.pem` file
- Use security groups to restrict SSH access to your IP only
- IAM roles provide secure credentials without embedding keys