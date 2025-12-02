"""
Green Software Foundation Patterns
Official patterns from https://patterns.greensoftware.foundation/

Categories: Cloud (40+ patterns), Web (15+ patterns), AI/ML (10+ patterns)
Total: 65+ official GSF patterns
"""

GSF_PATTERNS = {
    # ==================== CLOUD PATTERNS (40+) ====================
    "cache_static_data": {
        "name": "Cache Static Data",
        "category": "cloud",
        "keywords": ["cache", "caching", "static", "cdn", "redis", "memcache", "cached"],
        "description": "Cache static content to reduce server load and network transfers",
        "sci_impact": "Reduces energy by minimizing redundant compute and network operations"
    },
    "choose_region_closest": {
        "name": "Choose Region Closest to Users",
        "category": "cloud",
        "keywords": ["region", "closest", "proximity", "latency", "location", "geographic"],
        "description": "Deploy in regions closest to users to reduce network distance",
        "sci_impact": "Less energy for network transmission, lower latency"
    },
    "compress_stored_data": {
        "name": "Compress Stored Data",
        "category": "cloud",
        "keywords": ["compress", "compression", "stored", "storage", "gzip", "zstd"],
        "description": "Compress data at rest to reduce storage footprint",
        "sci_impact": "Lower embodied carbon from reduced storage infrastructure"
    },
    "compress_transmitted_data": {
        "name": "Compress Transmitted Data",
        "category": "cloud",
        "keywords": ["compress", "transmission", "gzip", "brotli", "network"],
        "description": "Compress data before transmission over network",
        "sci_impact": "Reduces network energy consumption and transfer time"
    },
    "containerize_workload": {
        "name": "Containerize Your Workload",
        "category": "cloud",
        "keywords": ["container", "docker", "kubernetes", "containerize", "pod"],
        "description": "Use containers for better resource utilization",
        "sci_impact": "Improved resource density and efficiency"
    },
    "delete_unused_storage": {
        "name": "Delete Unused Storage Resources",
        "category": "cloud",
        "keywords": ["delete", "remove", "unused", "storage", "cleanup", "orphan"],
        "description": "Remove storage resources that are no longer needed",
        "sci_impact": "Eliminates wasted energy and embodied carbon"
    },
    "encrypt_necessary": {
        "name": "Encrypt What Is Necessary",
        "category": "cloud",
        "keywords": ["encrypt", "encryption", "tls", "ssl", "crypto"],
        "description": "Only encrypt data that requires protection",
        "sci_impact": "Reduces CPU overhead from unnecessary encryption"
    },
    "evaluate_cpu_architectures": {
        "name": "Evaluate Other CPU Architectures",
        "category": "cloud",
        "keywords": ["cpu", "architecture", "arm", "graviton", "processor"],
        "description": "Consider ARM and other efficient CPU architectures",
        "sci_impact": "Some architectures offer better energy efficiency"
    },
    "service_mesh": {
        "name": "Evaluate Using a Service Mesh",
        "category": "cloud",
        "keywords": ["service mesh", "istio", "linkerd", "envoy"],
        "description": "Use service mesh for efficient service-to-service communication",
        "sci_impact": "Optimizes network traffic and observability overhead"
    },
    "tls_termination": {
        "name": "Evaluate TLS Termination",
        "category": "cloud",
        "keywords": ["tls", "termination", "ssl", "offload"],
        "description": "Terminate TLS at edge to reduce encryption overhead",
        "sci_impact": "Reduces CPU load on backend services"
    },
    "stateless_design": {
        "name": "Implement Stateless Design",
        "category": "cloud",
        "keywords": ["stateless", "state", "session", "horizontal"],
        "description": "Design services without server-side state",
        "sci_impact": "Enables better scaling and resource utilization"
    },
    "match_slo": {
        "name": "Match SLO Requirements",
        "category": "cloud",
        "keywords": ["slo", "sla", "service level", "objective"],
        "description": "Don't over-engineer beyond required SLO",
        "sci_impact": "Avoids wasted resources on unnecessary performance"
    },
    "match_vm_utilization": {
        "name": "Match VM Utilization Requirements",
        "category": "cloud",
        "keywords": ["vm", "virtual machine", "instance", "size", "utilization"],
        "description": "Right-size VMs to actual workload needs",
        "sci_impact": "Eliminates idle resources and wasted energy"
    },
    "minimize_environments": {
        "name": "Minimize Deployed Environments",
        "category": "cloud",
        "keywords": ["environment", "dev", "staging", "ephemeral"],
        "description": "Reduce number of permanent test/dev environments",
        "sci_impact": "Less idle infrastructure consuming energy"
    },
    "optimize_storage_utilization": {
        "name": "Optimize Storage Resource Utilization",
        "category": "cloud",
        "keywords": ["storage", "optimize", "utilization", "efficiency"],
        "description": "Maximize usage of provisioned storage",
        "sci_impact": "Better hardware efficiency, less waste"
    },
    "optimize_avg_cpu": {
        "name": "Optimize Average CPU Utilization",
        "category": "cloud",
        "keywords": ["cpu", "utilization", "average", "optimize"],
        "description": "Increase average CPU utilization across fleet",
        "sci_impact": "More work per unit of energy consumed"
    },
    "optimize_peak_cpu": {
        "name": "Optimize Peak CPU Utilization",
        "category": "cloud",
        "keywords": ["cpu", "peak", "spike", "burst"],
        "description": "Handle peaks efficiently without over-provisioning",
        "sci_impact": "Reduces need for excess capacity"
    },
    "queue_non_urgent": {
        "name": "Queue Non-Urgent Requests",
        "category": "cloud",
        "keywords": ["queue", "async", "batch", "defer", "background"],
        "description": "Queue non-urgent work for batch processing",
        "sci_impact": "Better resource utilization and scheduling"
    },
    "reduce_network_traversal": {
        "name": "Reduce Network Traversal Between VMs",
        "category": "cloud",
        "keywords": ["network", "traversal", "hop", "latency", "cross-az"],
        "description": "Minimize network hops between services",
        "sci_impact": "Less network equipment and energy per request"
    },
    "reduce_transmitted_data": {
        "name": "Reduce Transmitted Data",
        "category": "cloud",
        "keywords": ["reduce", "data", "transmission", "payload", "bandwidth"],
        "description": "Send only necessary data over network",
        "sci_impact": "Lower network energy consumption"
    },
    "remove_unused_assets": {
        "name": "Remove Unused Assets",
        "category": "cloud",
        "keywords": ["remove", "unused", "asset", "cleanup", "garbage"],
        "description": "Delete unused code, images, dependencies",
        "sci_impact": "Reduces storage and deployment footprint"
    },
    "scale_down_k8s": {
        "name": "Scale Down Kubernetes Workloads",
        "category": "cloud",
        "keywords": ["scale down", "kubernetes", "k8s", "downscale", "hpa"],
        "description": "Automatically scale down idle K8s workloads",
        "sci_impact": "Eliminates idle resource consumption"
    },
    "scale_down_apps": {
        "name": "Scale Down Unused Applications",
        "category": "cloud",
        "keywords": ["scale", "down", "idle", "suspend", "hibernate"],
        "description": "Scale down or shut down idle applications",
        "sci_impact": "Reduces energy from idle services"
    },
    "scale_with_load": {
        "name": "Scale Infrastructure with User Load",
        "category": "cloud",
        "keywords": ["autoscale", "scale", "elastic", "demand", "load"],
        "description": "Automatically scale based on actual demand",
        "sci_impact": "Matches resources to need, eliminates waste"
    },
    "k8s_event_scaling": {
        "name": "Scale Kubernetes Workloads Based on Events",
        "category": "cloud",
        "keywords": ["keda", "event", "scale", "kubernetes", "queue"],
        "description": "Scale based on queue depth or event metrics",
        "sci_impact": "Precise scaling to actual workload"
    },
    "scale_logical_components": {
        "name": "Scale Logical Components Independently",
        "category": "cloud",
        "keywords": ["microservice", "component", "independent", "decouple"],
        "description": "Scale services independently based on their load",
        "sci_impact": "Avoids scaling entire application for one bottleneck"
    },
    "scan_vulnerabilities": {
        "name": "Scan for Vulnerabilities",
        "category": "cloud",
        "keywords": ["security", "vulnerability", "scan", "cve"],
        "description": "Regular security scans to prevent breaches",
        "sci_impact": "Prevents energy waste from attacks and remediation"
    },
    "retention_policy": {
        "name": "Set Retention Policy on Storage",
        "category": "cloud",
        "keywords": ["retention", "policy", "lifecycle", "expire", "ttl"],
        "description": "Automatically delete old data per policy",
        "sci_impact": "Reduces storage footprint over time"
    },
    "shed_lower_priority": {
        "name": "Shed Lower Priority Traffic",
        "category": "cloud",
        "keywords": ["shed", "priority", "throttle", "rate limit", "backpressure"],
        "description": "Drop low-priority requests under load",
        "sci_impact": "Protects resources for important work"
    },
    "time_shift_cron": {
        "name": "Time-Shift Kubernetes Cron Jobs",
        "category": "cloud",
        "keywords": ["time shift", "cron", "schedule", "carbon aware", "renewable"],
        "description": "Run batch jobs when renewable energy is available",
        "sci_impact": "Uses cleaner energy sources"
    },
    "async_not_sync": {
        "name": "Use Async Instead of Sync",
        "category": "cloud",
        "keywords": ["async", "asynchronous", "non-blocking", "await"],
        "description": "Use asynchronous processing patterns",
        "sci_impact": "Better CPU utilization, less idle time"
    },
    "circuit_breaker": {
        "name": "Use Circuit Breaker",
        "category": "cloud",
        "keywords": ["circuit breaker", "fault tolerance", "resilience", "fallback"],
        "description": "Prevent cascading failures with circuit breakers",
        "sci_impact": "Avoids wasted energy on failing requests"
    },
    "cloud_native_security": {
        "name": "Use Cloud Native Security Tools",
        "category": "cloud",
        "keywords": ["security", "native", "managed", "cloud"],
        "description": "Use cloud provider's native security services",
        "sci_impact": "More efficient than running own security infrastructure"
    },
    "compiled_languages": {
        "name": "Use Compiled Languages",
        "category": "cloud",
        "keywords": ["compile", "compiled", "rust", "go", "c++"],
        "description": "Consider compiled languages for CPU-intensive tasks",
        "sci_impact": "Better runtime performance and energy efficiency"
    },
    "ddos_protection": {
        "name": "Use DDoS Protection",
        "category": "cloud",
        "keywords": ["ddos", "protection", "shield", "waf"],
        "description": "Protect against distributed denial of service",
        "sci_impact": "Prevents energy waste from malicious traffic"
    },
    "energy_efficient_hardware": {
        "name": "Use Energy Efficient Hardware",
        "category": "cloud",
        "keywords": ["energy", "efficient", "hardware", "green", "sustainable"],
        "description": "Choose hardware optimized for energy efficiency",
        "sci_impact": "Direct reduction in energy consumption"
    },
    
    # ==================== WEB PATTERNS (15+) ====================
    "avoid_chaining_requests": {
        "name": "Avoid Chaining Critical Requests",
        "category": "web",
        "keywords": ["chain", "critical", "request", "waterfall", "sequential"],
        "description": "Avoid serialized network requests that block rendering",
        "sci_impact": "Faster page load, less energy for rendering"
    },
    "avoid_excessive_dom": {
        "name": "Avoid Excessive DOM Size",
        "category": "web",
        "keywords": ["dom", "size", "excessive", "tree", "nodes"],
        "description": "Keep DOM tree small and shallow",
        "sci_impact": "Reduces memory and rendering energy"
    },
    "avoid_tracking_unnecessary": {
        "name": "Avoid Tracking Unnecessary Data",
        "category": "web",
        "keywords": ["tracking", "analytics", "telemetry", "unnecessary"],
        "description": "Don't track data you won't use",
        "sci_impact": "Reduces network and storage overhead"
    },
    "defer_offscreen_images": {
        "name": "Defer Offscreen Images",
        "category": "web",
        "keywords": ["defer", "offscreen", "image", "lazy load", "viewport"],
        "description": "Load images only when they enter viewport",
        "sci_impact": "Reduces initial load energy and bandwidth"
    },
    "deprecate_gifs": {
        "name": "Deprecate GIFs",
        "category": "web",
        "keywords": ["gif", "video", "webm", "mp4", "animation"],
        "description": "Use video formats instead of animated GIFs",
        "sci_impact": "Video formats are much more efficient than GIF"
    },
    "enable_text_compression": {
        "name": "Enable Text Compression",
        "category": "web",
        "keywords": ["compress", "text", "gzip", "brotli", "minify"],
        "description": "Compress HTML, CSS, JS before transmission",
        "sci_impact": "Reduces bandwidth and transfer energy"
    },
    "keep_request_counts_low": {
        "name": "Keep Request Counts Low",
        "category": "web",
        "keywords": ["request", "count", "http", "reduce", "combine"],
        "description": "Minimize number of HTTP requests",
        "sci_impact": "Lower network overhead per page load"
    },
    "minify_web_assets": {
        "name": "Minify Web Assets",
        "category": "web",
        "keywords": ["minify", "minification", "uglify", "compress"],
        "description": "Remove whitespace and unnecessary code",
        "sci_impact": "Smaller files, less bandwidth"
    },
    "minimize_main_thread": {
        "name": "Minimize Main Thread Work",
        "category": "web",
        "keywords": ["main thread", "worker", "offload", "javascript"],
        "description": "Offload work from main thread to web workers",
        "sci_impact": "Better CPU utilization, faster page loads"
    },
    "properly_sized_images": {
        "name": "Properly Sized Images",
        "category": "web",
        "keywords": ["image", "size", "resize", "responsive", "srcset"],
        "description": "Serve images at correct display size",
        "sci_impact": "Avoids transferring and processing oversized images"
    },
    "remove_unused_css": {
        "name": "Remove Unused CSS",
        "category": "web",
        "keywords": ["css", "unused", "purge", "tree shake"],
        "description": "Eliminate CSS that isn't used on page",
        "sci_impact": "Smaller CSS files, faster parsing"
    },
    "serve_modern_image_formats": {
        "name": "Serve Images in Modern Formats",
        "category": "web",
        "keywords": ["webp", "avif", "image", "format", "modern"],
        "description": "Use WebP or AVIF instead of JPEG/PNG",
        "sci_impact": "Modern formats are significantly more efficient"
    },
    "server_side_rendering": {
        "name": "Use Server-Side Rendering",
        "category": "web",
        "keywords": ["ssr", "server side", "rendering", "nextjs"],
        "description": "Pre-render pages on server when appropriate",
        "sci_impact": "Reduces client-side computation energy"
    },
    
    # ==================== AI/ML PATTERNS (10+) ====================
    "compress_ml_models": {
        "name": "Compress ML Models for Inference",
        "category": "ai",
        "keywords": ["compress", "model", "quantiz", "prune", "distill"],
        "description": "Reduce model size through quantization, pruning, distillation",
        "sci_impact": "Dramatically reduces inference energy and memory"
    },
    "efficient_format_training": {
        "name": "Efficient Format for Model Training",
        "category": "ai",
        "keywords": ["format", "training", "tfrecord", "parquet", "efficient"],
        "description": "Use efficient data formats for training",
        "sci_impact": "Faster I/O, less storage, quicker training"
    },
    "energy_efficient_ai_edge": {
        "name": "Energy Efficient AI at Edge",
        "category": "ai",
        "keywords": ["edge", "ai", "inference", "local", "device"],
        "description": "Run inference on edge devices when possible",
        "sci_impact": "Eliminates network transfer, uses local compute"
    },
    "energy_efficient_framework": {
        "name": "Energy Efficient Framework",
        "category": "ai",
        "keywords": ["framework", "tensorflow", "pytorch", "efficient"],
        "description": "Choose ML frameworks optimized for efficiency",
        "sci_impact": "Different frameworks have different energy profiles"
    },
    "energy_efficient_models": {
        "name": "Energy Efficient Models",
        "category": "ai",
        "keywords": ["model", "efficient", "mobilenet", "efficientnet"],
        "description": "Use models designed for efficiency (e.g., MobileNet)",
        "sci_impact": "Purpose-built efficient architectures"
    },
    "leverage_sustainable_regions_ai": {
        "name": "Leverage Sustainable Regions for AI",
        "category": "ai",
        "keywords": ["region", "sustainable", "renewable", "carbon"],
        "description": "Train models in regions with clean energy",
        "sci_impact": "Lower carbon intensity for training"
    },
    "pretrained_transfer_learning": {
        "name": "Pre-trained Transfer Learning",
        "category": "ai",
        "keywords": ["transfer", "learning", "pretrain", "fine-tune"],
        "description": "Start from pre-trained models instead of training from scratch",
        "sci_impact": "Avoids massive energy cost of full training"
    },
    "right_hardware_ai": {
        "name": "Right Hardware Type for AI",
        "category": "ai",
        "keywords": ["hardware", "gpu", "tpu", "accelerator", "ai"],
        "description": "Use appropriate hardware (GPU/TPU) for AI workloads",
        "sci_impact": "Specialized hardware is more energy efficient"
    },
    "serverless_ml": {
        "name": "Serverless Model Development",
        "category": "ai",
        "keywords": ["serverless", "ml", "sagemaker", "vertex", "lambda"],
        "description": "Use serverless platforms for ML development",
        "sci_impact": "Pay-per-use, no idle resources"
    },
    
    # ==================== GENERAL PATTERNS ====================
    "autoscaling": {
        "name": "Autoscaling",
        "category": "cloud",
        "keywords": ["autoscal", "scale", "elastic", "horizontal scaling", "hpa", "scaling policy"],
        "description": "Automatically scale resources based on demand",
        "sci_impact": "Reduces carbon emissions by matching resources to actual demand"
    },
    "optimize_storage": {
        "name": "Optimize Storage",
        "category": "cloud",
        "keywords": ["compress", "deduplicate", "archive", "storage tier", "lifecycle policy"],
        "description": "Reduce storage footprint through compression and deduplication",
        "sci_impact": "Lower embodied carbon through reduced storage infrastructure"
    },
    "serverless": {
        "name": "Use Serverless",
        "category": "cloud",
        "keywords": ["serverless", "lambda", "function", "faas", "cloud function"],
        "description": "Use serverless computing for event-driven workloads",
        "sci_impact": "Pay-per-use model ensures zero idle resource consumption"
    },
    "right_sizing": {
        "name": "Right-size Resources",
        "category": "cloud",
        "keywords": ["right-size", "rightsize", "downsize", "optimize instance", "resource optimization"],
        "description": "Match compute resources to actual workload requirements",
        "sci_impact": "Eliminates over-provisioning and reduces wasted energy"
    },
    
    # WEB PATTERNS
    "lazy_loading": {
        "name": "Lazy Loading",
        "category": "web",
        "keywords": ["lazy load", "lazy", "defer", "async", "on-demand"],
        "description": "Load resources only when needed",
        "sci_impact": "Reduces unnecessary data transfer and processing"
    },
    "minimize_data_transfer": {
        "name": "Minimize Data Transfer",
        "category": "web",
        "keywords": ["minif", "compress", "gzip", "brotli", "optimize payload", "reduce bundle"],
        "description": "Reduce size of data transferred over network",
        "sci_impact": "Lower network energy consumption and faster load times"
    },
    "optimize_images": {
        "name": "Optimize Images",
        "category": "web",
        "keywords": ["image optim", "webp", "responsive image", "lazy image", "compress image"],
        "description": "Use efficient image formats and sizing",
        "sci_impact": "Reduces bandwidth and storage requirements"
    },
    "reduce_http_requests": {
        "name": "Reduce HTTP Requests",
        "category": "web",
        "keywords": ["bundle", "sprite", "inline", "combine", "reduce request"],
        "description": "Minimize number of network requests",
        "sci_impact": "Lower network overhead and latency"
    },
    
    # AI/ML PATTERNS  
    "model_optimization": {
        "name": "Optimize ML Models",
        "category": "ai",
        "keywords": ["quantiz", "prune", "distill", "model compress", "optimize model"],
        "description": "Reduce model size and complexity",
        "sci_impact": "Dramatically reduces compute and memory requirements"
    },
    "batch_inference": {
        "name": "Batch Inference",
        "category": "ai",
        "keywords": ["batch inference", "batch predict", "batch processing"],
        "description": "Process ML predictions in batches",
        "sci_impact": "More efficient GPU utilization"
    },
    
    # NETWORKING PATTERNS
    "connection_pooling": {
        "name": "Connection Pooling",
        "category": "networking",
        "keywords": ["connection pool", "pool", "reuse connection", "persistent connection"],
        "description": "Reuse network connections instead of creating new ones",
        "sci_impact": "Reduces connection overhead and resource consumption"
    },
    "rate_limiting": {
        "name": "Rate Limiting",
        "category": "networking",
        "keywords": ["rate limit", "throttle", "backpressure", "circuit breaker"],
        "description": "Control request rate to prevent resource exhaustion",
        "sci_impact": "Prevents waste from processing excessive or malicious traffic"
    },
    
    # DATABASE PATTERNS
    "database_indexing": {
        "name": "Database Indexing",
        "category": "database",
        "keywords": ["index", "query optim", "explain", "slow query"],
        "description": "Optimize database queries with proper indexing",
        "sci_impact": "Reduces compute cycles for data retrieval"
    },
    "data_partitioning": {
        "name": "Data Partitioning",
        "category": "database",
        "keywords": ["partition", "shard", "segment", "distribute data"],
        "description": "Distribute data across multiple nodes",
        "sci_impact": "Improves query efficiency and resource utilization"
    },
    
    # GENERAL PATTERNS
    "async_processing": {
        "name": "Asynchronous Processing",
        "category": "general",
        "keywords": ["async", "asynchronous", "non-blocking", "event-driven", "queue"],
        "description": "Process tasks asynchronously to improve resource utilization",
        "sci_impact": "Better CPU utilization and reduced idle time"
    },
    "resource_pooling": {
        "name": "Resource Pooling",
        "category": "general",
        "keywords": ["thread pool", "worker pool", "object pool", "resource pool"],
        "description": "Reuse expensive resources instead of creating new ones",
        "sci_impact": "Reduces initialization overhead and memory pressure"
    },
    "memoization": {
        "name": "Memoization",
        "category": "general",
        "keywords": ["memoize", "memoization", "cache result", "remember"],
        "description": "Cache results of expensive function calls",
        "sci_impact": "Avoids redundant computation"
    },
    "batch_processing": {
        "name": "Batch Processing",
        "category": "general",
        "keywords": ["batch", "bulk", "batch insert", "batch update"],
        "description": "Process multiple items together instead of one at a time",
        "sci_impact": "Reduces per-item overhead and improves throughput"
    }
}

# Green software keywords (comprehensive list from all GSF patterns)
GREEN_KEYWORDS = [
    # Core sustainability terms
    "energy", "power", "carbon", "emission", "footprint", "sustainability", "sustainable", "green",
    "efficient", "efficiency", "eco", "environment", "renewable",
    
    # Performance & optimization
    "optimize", "optimization", "optimise", "optimisation", "performance", "performant",
    "fast", "faster", "speed", "speedup", "latency", "throughput", "utilization",
    
    # Caching & storage
    "cache", "caching", "cached", "redis", "memcache", "memcached", "cdn",
    "storage", "compress", "compression", "compressed", "gzip", "brotli", "zstd",
    "deduplicate", "dedup", "archive", "retention",
    
    # Resource management
    "pool", "pooling", "connection pool", "thread pool", "worker pool", "resource pool",
    "reuse", "recycle", "cleanup", "garbage", "remove unused", "delete unused",
    
    # Async & concurrency
    "async", "asynchronous", "non-blocking", "await", "promise", "queue",
    "background", "worker", "job", "batch", "batching",
    
    # Scaling & sizing
    "scale", "scaling", "autoscale", "autoscaling", "elastic", "elasticity",
    "horizontal", "vertical", "right-size", "rightsize", "downsize", "upsize",
    "hpa", "keda", "demand", "load",
    
    # Cloud native
    "serverless", "lambda", "function", "faas", "cloud function",
    "container", "docker", "kubernetes", "k8s", "pod",
    "microservice", "service mesh", "istio", "envoy",
    
    # Network optimization
    "network", "bandwidth", "transmission", "transfer", "latency", "proximity",
    "region", "closest", "edge", "cdn", "rate limit", "throttle", "backpressure",
    "circuit breaker", "shed", "reduce request", "minimize request",
    
    # Data & database
    "index", "indexing", "query", "optimize query", "query optimization",
    "partition", "shard", "database", "db", "sql", "nosql",
    
    # Web optimization
    "minify", "minification", "uglify", "tree shake", "bundle",
    "lazy load", "defer", "offscreen", "viewport", "dom",
    "ssr", "server side rendering", "hydration",
    "webp", "avif", "image", "responsive",
    
    # AI/ML
    "model", "quantiz", "prune", "pruning", "distill", "distillation",
    "inference", "training", "pretrain", "transfer learning",
    "gpu", "tpu", "accelerator", "mobilenet", "efficientnet",
    
    # Code & architecture
    "stateless", "decouple", "independent", "component",
    "compiled", "rust", "go", "c++",
    "refactor", "dead code", "unused", "deprecate",
    
    # Security (energy-related)
    "ddos", "vulnerability", "scan", "security", "waf",
    
    # Monitoring & SLO
    "slo", "sla", "metric", "monitor", "observability",
    
    # Specific technologies
    "redis", "memcached", "nginx", "envoy", "linkerd",
    "karpenter", "cluster autoscaler", "spot instance",
    "graviton", "arm", "architecture"
]

def get_pattern_by_keywords(commit_message: str) -> list:
    """
    Match commit message against GSF patterns.
    
    Args:
        commit_message: The commit message to analyze
        
    Returns:
        List of matched pattern names
    """
    message_lower = commit_message.lower()
    matched_patterns = []
    
    for pattern_id, pattern in GSF_PATTERNS.items():
        for keyword in pattern["keywords"]:
            if keyword.lower() in message_lower:
                matched_patterns.append(pattern["name"])
                break
    
    return matched_patterns

def is_green_aware(commit_message: str) -> bool:
    """
    Check if commit shows green software awareness.
    
    Args:
        commit_message: The commit message to analyze
        
    Returns:
        True if commit contains green keywords
    """
    message_lower = commit_message.lower()
    return any(keyword.lower() in message_lower for keyword in GREEN_KEYWORDS)
