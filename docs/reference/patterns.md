# GSF Patterns Reference

Complete reference for all 122 Green Software Foundation patterns supported by GreenMining.

---

## Overview

GreenMining detects patterns from the [Green Software Foundation](https://patterns.greensoftware.foundation/) catalog, organized into 15 categories.

| Statistic | Value |
|-----------|-------|
| **Total Patterns** | 122 |
| **Categories** | 15 |
| **Keywords** | 321 |

---

## Pattern Categories

### Cloud Patterns (40+)

Patterns for cloud-native and infrastructure optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Cache Static Data | cache, caching, static, cdn, redis, memcache | Cache static content to reduce server load |
| Choose Region Closest | region, closest, proximity, latency | Deploy in regions closest to users |
| Compress Stored Data | compress, storage, gzip, zstd | Compress data at rest |
| Compress Transmitted Data | compress, transmission, gzip, brotli | Compress data before network transfer |
| Containerize Workload | container, docker, kubernetes, pod | Use containers for resource efficiency |
| Delete Unused Storage | delete, remove, unused, cleanup | Remove unused storage resources |
| Encrypt What Is Necessary | encrypt, tls, ssl, crypto | Only encrypt data that needs protection |
| Evaluate CPU Architectures | cpu, arm, graviton, processor | Consider ARM and efficient CPUs |
| Use Service Mesh | service mesh, istio, linkerd, envoy | Optimize service-to-service communication |
| TLS Termination | tls termination, ssl offload | Terminate TLS at edge |
| Implement Stateless Design | stateless, session, horizontal | Design without server-side state |
| Match SLO Requirements | slo, sla, service level | Don't over-engineer beyond SLO |
| Match VM Utilization | vm, instance, size, utilization | Right-size VMs to workload |
| Move to Cloud | cloud, migrate, migration | Leverage cloud efficiency |
| Optimize Average Utilization | utilization, optimize, average | Increase resource utilization |
| Optimize High Utilization | high utilization, maximize | Target high utilization levels |
| Optimize Network Traffic | network, traffic, optimize | Reduce unnecessary network traffic |
| Scale Down Idle Resources | scale down, idle, shutdown | Reduce resources when idle |
| Scale Infrastructure | scaling, autoscaling, scale | Scale based on demand |
| Terminate Unused Resources | terminate, unused, cleanup | Remove unused resources |
| Use Reserved Instances | reserved, spot, savings | Use cost-efficient instance types |
| Use Serverless | serverless, lambda, functions | Use serverless for variable workloads |
| Use Spot Instances | spot, preemptible, interruption | Use spot instances for cost savings |

### Web Patterns (15+)

Patterns for web application optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Enable Text Compression | gzip, brotli, deflate | Compress text responses |
| Lazy Loading | lazy, defer, on-demand | Load content only when needed |
| Minify CSS/JS | minify, minification, uglify | Reduce asset file sizes |
| Optimize Images | image, webp, avif, srcset | Use modern image formats |
| Use CDN | cdn, content delivery, edge | Serve from edge locations |
| Cache HTTP Responses | cache-control, etag, expires | Enable browser caching |
| Reduce DOM Size | dom, elements, optimize | Minimize DOM complexity |
| Use Service Workers | service worker, pwa, offline | Enable offline caching |
| Preconnect Resources | preconnect, preload, prefetch | Hint browser to connect early |
| Remove Unused CSS | unused, purge, tree-shake | Remove dead CSS code |
| Optimize Fonts | font, woff2, subset | Use efficient font loading |
| Reduce JavaScript | javascript, bundle, split | Minimize JS payload |
| Use HTTP/2 | http2, multiplexing | Use modern HTTP protocol |
| Enable Keep-Alive | keep-alive, persistent | Reuse HTTP connections |

### AI/ML Patterns (10+)

Patterns for machine learning optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Model Optimization | model, optimize, prune | Optimize model architecture |
| Quantization | quantize, int8, fp16 | Reduce model precision |
| Knowledge Distillation | distillation, student, teacher | Train smaller models |
| Efficient Training | training, efficient, epoch | Optimize training process |
| Batch Inference | batch, inference, throughput | Process predictions in batches |
| Model Caching | model cache, warm, preload | Cache loaded models |
| Feature Selection | feature, select, reduce | Use fewer features |
| Early Stopping | early stop, convergence | Stop training when converged |
| Mixed Precision | mixed precision, amp | Use mixed precision training |
| Gradient Checkpointing | checkpoint, gradient, memory | Trade compute for memory |

### Caching Patterns (8)

Patterns for caching strategies.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Redis Caching | redis, cache, memory | Use Redis for caching |
| CDN Caching | cdn, edge, cache | Cache at CDN edge |
| Database Query Cache | query cache, mysql, postgres | Cache database queries |
| Application Cache | app cache, memory, local | In-memory application cache |
| Distributed Cache | distributed, memcached | Multi-node caching |
| Cache Invalidation | invalidate, ttl, expire | Proper cache expiration |
| Write-Through Cache | write-through, consistency | Consistent caching |
| Cache Warming | warm, preload, prefetch | Pre-populate caches |

### Async Patterns (6)

Patterns for asynchronous processing.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Queue Non-Urgent Requests | queue, async, defer | Queue non-critical work |
| Use Async Instead of Sync | async, await, non-blocking | Prefer async operations |
| Batch Processing | batch, bulk, aggregate | Process in batches |
| Event-Driven Architecture | event, pub-sub, message | Use event-driven design |
| Background Jobs | background, worker, job | Process in background |
| Stream Processing | stream, reactive, flow | Use streaming for large data |

### Database Patterns (8)

Patterns for database optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Optimize Database Queries | query, optimize, explain | Improve query performance |
| Use Connection Pooling | pool, connection, reuse | Reuse database connections |
| Index Optimization | index, btree, covering | Optimize database indexes |
| Read Replicas | replica, read, slave | Scale reads with replicas |
| Denormalization | denormalize, join, embed | Reduce join operations |
| Partition Tables | partition, shard, split | Split large tables |
| Use NoSQL | nosql, document, key-value | Use appropriate database type |
| Lazy Loading Relations | lazy, eager, n+1 | Avoid N+1 query problems |

### Network Patterns (6)

Patterns for network optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| HTTP Compression | gzip, compress, transfer | Compress HTTP responses |
| Reduce API Calls | batch, aggregate, graphql | Minimize API requests |
| Use WebSockets | websocket, socket, realtime | Use persistent connections |
| Protocol Optimization | http3, quic, protocol | Use efficient protocols |
| Edge Computing | edge, close, proximity | Process at the edge |
| Connection Reuse | keep-alive, persist, reuse | Reuse network connections |

### Resource Patterns (5)

Patterns for resource management.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Memory Optimization | memory, heap, gc | Optimize memory usage |
| CPU Optimization | cpu, thread, parallel | Optimize CPU usage |
| I/O Optimization | io, disk, buffer | Optimize I/O operations |
| Resource Pooling | pool, reuse, recycle | Pool expensive resources |
| Garbage Collection Tuning | gc, tuning, generational | Tune GC parameters |

### Code Patterns (4)

Patterns for code-level optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Remove Dead Code | dead code, unused, remove | Eliminate unused code |
| Algorithm Optimization | algorithm, complexity, O(n) | Use efficient algorithms |
| Loop Optimization | loop, iteration, vectorize | Optimize loops |
| Avoid Premature Optimization | premature, profile, measure | Profile before optimizing |

### Infrastructure Patterns (4)

Patterns for infrastructure optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Alpine Containers | alpine, minimal, scratch | Use minimal base images |
| Infrastructure as Code | iac, terraform, ansible | Manage infrastructure as code |
| Renewable Energy Regions | renewable, green, carbon | Use green energy regions |
| Container Optimization | container, layer, cache | Optimize container builds |

### Microservices Patterns (4)

Patterns for microservices architecture.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Service Decomposition | decompose, microservice, split | Right-size services |
| Colocation Strategies | colocate, affinity, proximity | Place related services together |
| Graceful Shutdown | graceful, shutdown, sigterm | Handle shutdown properly |
| Service Mesh Optimization | mesh, sidecar, istio | Optimize service mesh overhead |

### Monitoring Patterns (3)

Patterns for observability optimization.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Efficient Logging | logging, log level, structured | Optimize log volume |
| Metrics Aggregation | metrics, aggregate, rollup | Aggregate metrics efficiently |
| Trace Sampling | sampling, trace, opentelemetry | Sample traces appropriately |

### General Patterns (8)

General optimization patterns.

| Pattern | Keywords | Description |
|---------|----------|-------------|
| Feature Flags | feature flag, toggle, switch | Use feature flags |
| Incremental Processing | incremental, delta, diff | Process only changes |
| Precomputation | precompute, materialize, cache | Precompute expensive results |
| Background Jobs | background, async, worker | Process in background |
| Rate Limiting | rate limit, throttle, backoff | Limit request rates |
| Circuit Breaker | circuit, breaker, fallback | Fail fast with fallbacks |
| Retry with Backoff | retry, backoff, exponential | Retry with exponential backoff |
| Timeout Configuration | timeout, deadline, cancel | Set appropriate timeouts |

---

## Accessing Patterns Programmatically

```python
from greenmining import GSF_PATTERNS

# Count patterns
print(f"Total patterns: {len(GSF_PATTERNS)}")  # 122

# Get all categories
categories = set(p["category"] for p in GSF_PATTERNS.values())
print(f"Categories: {sorted(categories)}")

# Find patterns by category
cloud_patterns = [
    p for p in GSF_PATTERNS.values() 
    if p["category"] == "cloud"
]
print(f"Cloud patterns: {len(cloud_patterns)}")

# Get pattern details
pattern = GSF_PATTERNS["cache_static_data"]
print(f"Name: {pattern['name']}")
print(f"Category: {pattern['category']}")
print(f"Keywords: {pattern['keywords']}")
print(f"Description: {pattern['description']}")
print(f"SCI Impact: {pattern['sci_impact']}")
```

---

## Green Keywords

The 321 green keywords used for detection:

```python
from greenmining import GREEN_KEYWORDS

# Categories of keywords
keyword_categories = {
    "energy": ["energy", "power", "watt", "joule", "consumption"],
    "carbon": ["carbon", "emission", "co2", "greenhouse", "footprint"],
    "efficiency": ["efficient", "efficiency", "optimize", "reduce", "minimize"],
    "sustainability": ["sustainable", "green", "eco", "environmental"],
    "performance": ["performance", "fast", "speed", "latency", "throughput"],
    "resource": ["resource", "memory", "cpu", "disk", "network"],
    "caching": ["cache", "cached", "caching", "redis", "memcache"],
    "compression": ["compress", "gzip", "brotli", "minify", "compact"],
}

# Sample keywords
print(GREEN_KEYWORDS[:20])
# ['energy', 'power', 'carbon', 'emission', 'footprint', 'sustainability', ...]
```

---

## Pattern Detection Example

```python
from greenmining import is_green_aware, get_pattern_by_keywords

# Test messages
messages = [
    "Implement Redis caching for user sessions",
    "Enable gzip compression on API responses",
    "Migrate to serverless Lambda functions",
    "Optimize database queries with proper indexing",
    "Add lazy loading for images",
    "Fix typo in documentation",
]

for msg in messages:
    is_green = is_green_aware(msg)
    patterns = get_pattern_by_keywords(msg) if is_green else []
    
    if is_green:
        print(f"🌱 {msg}")
        print(f"   Patterns: {patterns}")
    else:
        print(f"   {msg}")
```

**Output:**

```
🌱 Implement Redis caching for user sessions
   Patterns: ['Cache Static Data']
🌱 Enable gzip compression on API responses
   Patterns: ['Compress Transmitted Data', 'Enable Text Compression']
🌱 Migrate to serverless Lambda functions
   Patterns: ['Use Serverless']
🌱 Optimize database queries with proper indexing
   Patterns: ['Optimize Database Queries', 'Index Optimization']
🌱 Add lazy loading for images
   Patterns: ['Lazy Loading', 'Optimize Images']
   Fix typo in documentation
```

---

## Contributing Patterns

To suggest new patterns or improvements:

1. Check the [GSF Patterns Catalog](https://patterns.greensoftware.foundation/)
2. Open an issue on [GitHub](https://github.com/adam-bouafia/greenmining/issues)
3. Submit a pull request with pattern additions

---

## Next Steps

- [Configuration Options](config-options.md) - All configuration parameters
- [Python API](../user-guide/api.md) - Programmatic usage
- [Data Models](models.md) - Repository and Commit models
