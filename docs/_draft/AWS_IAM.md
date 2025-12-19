# 1. IAM Policy ->
Can *THIS* identity perform *THIS* action on *THIS* resource?

A policy has:
1. Effect: Allow or Deny
2. Action: The action to perform
3. Resource: ARN of what the action is performed on

Rules:
* Policies are stateless
* Evaluates on a per-request basis
* Explicit Deny overrides Allow

Example:
```json
{
    "Effect": "Allow",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
}
```

# 2. Identity-based vs Resource-based policies
## Identity-based
### Attached to:
* Users
* Groups
* Roles

### Says: “What this identity can do”

### Used by:
* EC2
* ECS
* Lambda
* Humans (via users/groups)

## Resource-based
### Attached to:
* S3 buckets
* SQS queues
* SNS topics

### Says: “Who can access this resource”

AWS IAM — Level 2 (Trust Policy Deep Dive)
What this policy is
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["sts:AssumeRole"],
      "Principal": {
        "Service": ["ec2.amazonaws.com"]
      }
    }
  ]
}


This is a Trust Policy.

A trust policy defines WHO is allowed to assume an IAM role.

It does not define permissions like S3 access or CloudWatch access.

Key components explained
Version
"Version": "2012-10-17"


Policy language version

Almost always this value

Not related to AWS service versions

Effect
"Effect": "Allow"


Allows the specified principal to perform the action

Trust policies almost always use Allow

Explicit deny here would block role assumption

Action
"Action": ["sts:AssumeRole"]


Critical action in all trust policies

Means:

“This principal is allowed to assume this role”

Without sts:AssumeRole, the role cannot be assumed.

Principal
"Principal": {
  "Service": ["ec2.amazonaws.com"]
}


Defines who can assume the role

In this case:

Any EC2 instance is allowed (when attached to this role)

Other possible principals:

ecs-tasks.amazonaws.com

lambda.amazonaws.com

AWS account IDs

IAM users or roles (cross-account access)

What this policy DOES

✔ Allows EC2 instances to assume the role
✔ Enables temporary credentials via STS
✔ Allows AWS services to act securely without keys

What this policy DOES NOT do

❌ Does NOT grant access to CloudWatch
❌ Does NOT grant access to S3
❌ Does NOT define what actions are allowed

Those are handled by permission policies, attached separately.

Trust Policy vs Permission Policy (important distinction)
Trust Policy

Question answered:

Who can assume this role?

Uses:

Principal

sts:AssumeRole

Attached to the role itself

Permission Policy

Question answered:

What can the role do after being assumed?

Uses:

Action

Resource

Attached to the role as permissions

Both are required for a working role.

Real-world flow (connect it to practice)
EC2 Instance
  ↓
Assumes IAM Role (via Trust Policy)
  ↓
Gets Temporary Credentials (STS)
  ↓
Uses Permission Policy
  ↓
Writes logs to CloudWatch / accesses AWS APIs


No access keys in code. Ever.

Key takeaway (write this line)

A trust policy controls WHO can assume a role, not WHAT the role can do.

This single sentence prevents most IAM mistakes.