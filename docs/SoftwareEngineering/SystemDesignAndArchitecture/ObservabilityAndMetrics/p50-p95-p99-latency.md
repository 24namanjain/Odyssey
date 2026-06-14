---
title: p50, p95, p99 Latency
tags: [latency, percentiles, observability, metrics, system-design]
---

# p50, p95, p99 Latency

**The Core Concepts (Latency Percentiles)**

Percentiles tell you how a specific percentage of your users experience your system's speed. They prevent your metrics from being distorted by occasional outliers.

- **p50 (Median)**
  - The exact middle performance of your system—50% of requests are faster than this, and 50% are slower.
  - *Example:* If your p50 is 100ms, a typical, average user experiences a 100ms response time.

- **p95**
  - The threshold where 95% of requests are faster, and only the slowest 5% experience worse delay.
  - *Example:* If your p95 is 400ms, it means 95 out of 100 users get their data in under 400ms, while 5 users wait longer.

- **p99**
  - The edge-case metric where 99% of requests are faster, isolating the worst 1% of slow requests.
  - *Example:* If your p99 is 2 seconds, 1 out of 100 users hits a severe bottleneck (like cold starts or heavy database locks) and waits a full 2 seconds.

- **p99.9 (The "Tail" Latency)**
  - The extreme bottleneck layer, where only 0.1% of requests are slower than this value.
  - *Example:* At a scale of 1 million requests, a p99.9 of 5 seconds means 1,000 of your highest-scale requests are painfully slow.
