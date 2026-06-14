# EC2 – Phase 1: Launching an Instance (FOUNDATION)

## Details (Teaching / Conceptual Understanding)

### What is EC2?

Amazon EC2 (Elastic Compute Cloud) provides virtual machines in the cloud.

An EC2 instance is:
- A virtual computer
- Running an operating system
- Fully controlled by you
- Billed based on runtime + size

**EC2 is not serverless:**
- You manage lifecycle (start/stop/terminate)
- You manage security
- You manage OS-level access

### What happens when you “launch” an EC2 instance?

You are explicitly defining:
- What OS the machine runs
- How powerful it is
- Who can access it
- From where
- How storage is attached
- How much it will cost

AWS asks many questions because defaults would be unsafe or expensive.

### AMI (Amazon Machine Image)

An AMI is a template for the instance. It contains:
- Operating system
- Pre-installed tools

**We chose:** Amazon Linux 2023

**Why:**
- AWS-maintained
- Secure defaults
- Best integration with AWS services
- Free Tier friendly

> 📌 Changing AMI = changing the entire machine environment.

### Instance Type

**We selected:** `t2.micro`

Instance type defines:
- CPU
- Memory
- Network performance

**Why `t2.micro`:**
- Free Tier eligible
- Enough for learning
- Low cost risk

> 📌 Most AWS cost mistakes happen here.

### Key Pair (SSH Access)

Key pair = authentication mechanism.
- AWS stores only the public key
- You download and keep the private key (`.pem`)

**Important rules:**
- AWS will NOT recover lost private keys
- Without the key → instance is unreachable
- This replaces password-based login
- This is not optional for Linux EC2.

### Security Groups (Firewall)

A security group is a **stateful firewall** around EC2.

**Default behavior:**
- All inbound traffic ❌ blocked
- All outbound traffic ✅ allowed

**We configured:**

| Type | Port | Source |
|------|------|--------|
| SSH | 22 | My IP |
| HTTP | 80 | Anywhere |

**Why:**
- SSH restricted to your IP (security)
- HTTP open for learning purposes

> 📌 If security group blocks traffic, the OS never sees it.

### Storage (EBS – Elastic Block Store)

Root volume attached to EC2.
- **Size:** 8 GiB
- **Type:** gp3

**Concepts:**
- Acts like a disk
- Persists across stop/start
- Deleted on terminate (by default)

We did not modify storage yet — see [EC2 Instance Storage](../4-ec2-instance-storage/index.md) for EBS, snapshots, AMIs, and EFS.

### IAM Role (Intentionally Skipped)

We launched EC2 without an IAM role.

**Why:** To later observe what fails without permissions and why roles are necessary. This will reinforce IAM concepts practically.

### Instance Lifecycle (Very Important)

An EC2 instance can be:
- **Running** → billable
- **Stopped** → not billed for compute
- **Terminated** → destroyed permanently

> 📌 Stopping ≠ terminating.

## Console paths

> **Launch instance:** `AWS Console` › `EC2` › `Instances` › `Launch instance`

> **View instance details:** `AWS Console` › `EC2` › `Instances` › select instance

> **Security group settings:** `AWS Console` › `EC2` › `Instances` › `Security` tab › `Security groups`

> **Key pairs:** `AWS Console` › `EC2` › `Network & Security` › `Key pairs`

> **Instance state:** `AWS Console` › `EC2` › `Instances` › `Instance state`

> **Instance storage (EBS, EFS):** see [EC2 Instance Storage](../4-ec2-instance-storage/index.md)

## FAQs & Interview / Certification Q&A

**Q: What is an EC2 instance?**
A virtual machine provided by AWS where you manage OS, runtime, and lifecycle.

**Q: What is an AMI?**
A template containing the operating system and initial configuration for an EC2 instance.

**Q: Why is EC2 unreachable by default?**
Because inbound traffic is blocked unless explicitly allowed by security groups.

**Q: What happens if you lose the key pair?**
You lose SSH access to the instance.

**Q: Is EC2 billed when stopped?**
No (compute is not billed), but storage may still be billed.

**Q: Why is t2.micro commonly used for learning?**
It is Free Tier eligible and minimizes cost risk.

**Q: What controls network access to EC2?**
Security Groups (primary) and later NACLs (advanced).

## Current Status Checkpoint ✅

You have successfully:
- Launched an EC2 instance
- Chosen AMI correctly
- Selected a cost-safe instance type
- Created and used a key pair
- Configured security groups intentionally
- Understood instance lifecycle implications

You are now ready to:
👉 Connect to the instance (SSH)

### 🔒 End-of-Day Safety Reminder
Your instance is:
- **Running**
- **Billable** (Free Tier but still real)

We will:
1. SSH briefly
2. Learn
3. Stop/terminate intentionally
