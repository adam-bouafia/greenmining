# Mining Software Repositories for Green Microservices
## Comprehensive Analysis Report

**Report Generated:** 2026-01-07 21:29:05
**Analysis Type:** Keyword and Heuristic-Based Pattern Detection

---

### Executive Summary

This report presents findings from analyzing **39,664 commits** across **100 microservice-based repositories** to identify green software engineering practices.

**Key Findings:**

- **46.0%** of commits (18,253) explicitly mention energy efficiency, performance optimization, or sustainability concerns
- **98** out of 100 repositories contain at least one green-aware commit
- The most common patterns detected include: Keep Request Counts Low (4281 occurrences), Use Compiled Languages (3715 occurrences), Delete Unused Storage Resources (3493 occurrences).

**Implications:**

These findings suggest that while green software practices are present in microservices development, there is significant room for increased awareness and adoption of energy-efficient patterns. The relatively low percentage of green-aware commits indicates an opportunity for the software engineering community to emphasize sustainability in distributed systems.

### 1. Methodology

#### 1.1 Repository Selection Criteria

Repositories were selected from GitHub based on the following criteria:

- **Keywords:** microservices, cloud-native, energy-efficient, sustainable, performance-optimization, memory-efficient, event-driven, scalable
- **Programming Languages:** Python, Java, Go, JavaScript, TypeScript, C#, Rust, Kotlin, Ruby, C++
- **Minimum Stars:** 100 (to ensure established projects)
- **Sort Order:** Stars (descending)
- **Total Repositories:** 100

#### 1.2 Data Extraction Approach

Commit data was extracted using PyDriller library:

- **Commits Analyzed:** 0
- **Time Window:** Last 2 years (730 days)
- **Merge Commits:** Excluded
- **Minimum Commit Message Length:** 10 characters

#### 1.3 Analysis Methodology

Commits were analyzed using a keyword and heuristic-based classification framework:

**Q1) Green Awareness Detection:**
- Searched for explicit mentions of energy, performance, sustainability, caching, optimization, and related keywords
- Analyzed file names for patterns (cache, performance, optimization)

**Q2) Known Pattern Detection:**
- Matched against predefined green software tactics:
  - Resource pooling (connection pools, thread pools)
  - Caching strategies (Redis, in-memory caches)
  - Lazy initialization
  - Database query optimization
  - Asynchronous processing
  - Code optimization
  - Event-driven architecture
  - Resource limits
  - Service decommissioning
  - Auto-scaling

**Q3) Emergent Pattern Detection:**
- Placeholder for manual review of novel microservice-specific patterns

#### 1.4 Limitations and Scope

- Analysis based on commit messages and file names only (no code inspection)
- Keyword matching may miss implicit green practices
- Limited to English language commit messages
- Focused on microservices architecture
- 2-year time window may not capture all historical practices

### 2. Results

#### 2.1 Green Awareness in Commits

**Total commits analyzed:** 39,664
**Commits with explicit green mention:** 18,253 (46.0%)

**Table: Top 10 Repositories with Highest Green Awareness**

| Repository | Total Commits | Green Commits | Percentage |
|------------|---------------|---------------|------------|
| moby/moby | 500 | 487 | 97.4% |
| pingcap/tidb | 500 | 478 | 95.6% |
| webyog/sqlyog-community | 132 | 118 | 89.4% |
| paiml/depyler | 500 | 445 | 89.0% |
| cockroachdb/cockroach | 500 | 426 | 85.2% |
| sustainable-computing-io/kepler | 299 | 252 | 84.3% |
| milvus-io/milvus | 500 | 405 | 81.0% |
| envoyproxy/envoy | 500 | 381 | 76.2% |
| Stirling-Tools/Stirling-PDF | 500 | 367 | 73.4% |
| openfaas/faas | 500 | 365 | 73.0% |


**Table: Green Awareness by Programming Language**

| Language | Total Commits | Green Commits | Percentage |
|----------|---------------|---------------|------------|
| Python | 10,708 | 4,247 | 39.7% |
| Go | 10,069 | 6,128 | 60.9% |
| JavaScript | 4,356 | 1,468 | 33.7% |
| TypeScript | 3,841 | 1,532 | 39.9% |
| C++ | 3,214 | 1,705 | 53.0% |
| Rust | 3,082 | 1,744 | 56.6% |
| Java | 2,998 | 853 | 28.5% |
| Ruby | 781 | 264 | 33.8% |
| C# | 615 | 312 | 50.7% |


#### 2.2 Known Green Patterns & Tactics Applied

The following table summarizes the known green software patterns detected in the dataset:

**Table: Known Patterns Ranked by Frequency**

| Pattern | Count | Percentage | High Conf. | Medium Conf. | Low Conf. |
|---------|-------|------------|------------|--------------|----------|
| Keep Request Counts Low | 4,281 | 7.4% | 3591 | 690 | 0 |
| Use Compiled Languages | 3,715 | 6.4% | 2442 | 1273 | 0 |
| Delete Unused Storage Resources | 3,493 | 6.0% | 3350 | 143 | 0 |
| Remove Unused Assets | 3,000 | 5.2% | 2997 | 3 | 0 |
| Use Serverless | 1,934 | 3.3% | 1432 | 502 | 0 |
| Minimize Deployed Environments | 1,902 | 3.3% | 1517 | 385 | 0 |
| Reduce Transmitted Data | 1,776 | 3.1% | 1443 | 333 | 0 |
| Serve Images in Modern Formats | 1,630 | 2.8% | 1617 | 13 | 0 |
| Resource Limits & Constraints | 1,427 | 2.5% | 1012 | 415 | 0 |
| Containerize Your Workload | 1,412 | 2.4% | 984 | 428 | 0 |
| Scale Infrastructure with User Load | 1,266 | 2.2% | 1008 | 258 | 0 |
| Scale Kubernetes Workloads Based on Events | 1,170 | 2.0% | 1044 | 126 | 0 |
| Properly Sized Images | 1,158 | 2.0% | 1151 | 7 | 0 |
| Match VM Utilization Requirements | 1,123 | 1.9% | 1001 | 122 | 0 |
| Performance Profiling | 1,090 | 1.9% | 745 | 345 | 0 |
| Avoid Excessive DOM Size | 1,086 | 1.9% | 967 | 119 | 0 |
| Eliminate Polling | 1,018 | 1.8% | 820 | 198 | 0 |
| Efficient Format for Model Training | 1,011 | 1.8% | 1000 | 11 | 0 |
| Avoid Chaining Critical Requests | 931 | 1.6% | 883 | 48 | 0 |
| Match SLO Requirements | 878 | 1.5% | 627 | 251 | 0 |
| Cache Static Data | 840 | 1.5% | 607 | 233 | 0 |
| Enable Text Compression | 803 | 1.4% | 636 | 167 | 0 |
| Database Views & Materialized Views | 780 | 1.4% | 640 | 140 | 0 |
| Scale Down Unused Applications | 758 | 1.3% | 672 | 86 | 0 |
| Evaluate Other CPU Architectures | 758 | 1.3% | 601 | 157 | 0 |
| Defer Offscreen Images | 748 | 1.3% | 748 | 0 | 0 |
| Implement Stateless Design | 723 | 1.3% | 599 | 124 | 0 |
| Use Cloud Native Security Tools | 722 | 1.2% | 604 | 118 | 0 |
| Energy Efficient Models | 713 | 1.2% | 454 | 259 | 0 |
| Optimize Storage Resource Utilization | 667 | 1.2% | 664 | 3 | 0 |
| Database Indexing | 605 | 1.0% | 423 | 182 | 0 |
| Incremental Processing | 591 | 1.0% | 503 | 88 | 0 |
| Right Hardware Type for AI | 587 | 1.0% | 412 | 175 | 0 |
| Queue Non-Urgent Requests | 586 | 1.0% | 572 | 14 | 0 |
| Optimize Average CPU Utilization | 558 | 1.0% | 557 | 1 | 0 |
| Reduce Network Traversal Between VMs | 538 | 0.9% | 496 | 42 | 0 |
| Scan for Vulnerabilities | 469 | 0.8% | 431 | 38 | 0 |
| Remove Unused CSS | 465 | 0.8% | 421 | 44 | 0 |
| Compress Transmitted Data | 456 | 0.8% | 456 | 0 | 0 |
| Compress Stored Data | 432 | 0.7% | 425 | 7 | 0 |
| Feature Flags for Resource Control | 423 | 0.7% | 332 | 91 | 0 |
| Avoid Tracking Unnecessary Data | 408 | 0.7% | 365 | 43 | 0 |
| Scale Logical Components Independently | 363 | 0.6% | 294 | 69 | 0 |
| Set Retention Policy on Storage | 355 | 0.6% | 294 | 61 | 0 |
| Choose Region Closest to Users | 345 | 0.6% | 305 | 40 | 0 |
| Data Deduplication | 327 | 0.6% | 286 | 41 | 0 |
| Use Energy Efficient Hardware | 321 | 0.6% | 267 | 54 | 0 |
| Deprecate GIFs | 304 | 0.5% | 248 | 56 | 0 |
| Asynchronous Processing | 288 | 0.5% | 288 | 0 | 0 |
| Time-Shift Kubernetes Cron Jobs | 285 | 0.5% | 210 | 75 | 0 |
| Encrypt What Is Necessary | 269 | 0.5% | 246 | 23 | 0 |
| Scale Down Kubernetes Workloads | 262 | 0.5% | 227 | 35 | 0 |
| Batch Processing | 262 | 0.5% | 251 | 11 | 0 |
| gRPC for Service Communication | 261 | 0.5% | 219 | 42 | 0 |
| Data Partitioning | 258 | 0.4% | 195 | 63 | 0 |
| Lazy Loading | 230 | 0.4% | 228 | 2 | 0 |
| Optimize Peak CPU Utilization | 222 | 0.4% | 221 | 1 | 0 |
| Shed Lower Priority Traffic | 216 | 0.4% | 191 | 25 | 0 |
| Minimize Main Thread Work | 198 | 0.3% | 150 | 48 | 0 |
| Reduce HTTP Requests | 196 | 0.3% | 143 | 53 | 0 |
| Autoscaling | 191 | 0.3% | 188 | 3 | 0 |
| Leverage Sustainable Regions for AI | 184 | 0.3% | 163 | 21 | 0 |
| Evaluate TLS Termination | 180 | 0.3% | 180 | 0 | 0 |
| Evaluate Using a Service Mesh | 172 | 0.3% | 158 | 14 | 0 |
| Use Async Instead of Sync | 164 | 0.3% | 163 | 1 | 0 |
| Efficient Serialization | 162 | 0.3% | 128 | 34 | 0 |
| Model Quantization | 160 | 0.3% | 144 | 16 | 0 |
| Energy Efficient Framework | 158 | 0.3% | 141 | 17 | 0 |
| Cache Invalidation Strategy | 142 | 0.2% | 140 | 2 | 0 |
| API Gateway Pattern | 140 | 0.2% | 112 | 28 | 0 |
| Use Circuit Breaker | 139 | 0.2% | 119 | 20 | 0 |
| Connection Pooling | 135 | 0.2% | 111 | 24 | 0 |
| Efficient ML Framework | 125 | 0.2% | 125 | 0 | 0 |
| Optimize Storage | 122 | 0.2% | 116 | 6 | 0 |
| Event-Driven Architecture | 103 | 0.2% | 56 | 47 | 0 |
| Use Server-Side Rendering | 102 | 0.2% | 72 | 30 | 0 |
| Optimize ML Models | 101 | 0.2% | 101 | 0 | 0 |
| Minimize Data Transfer | 89 | 0.2% | 81 | 8 | 0 |
| Approximation Algorithms | 83 | 0.1% | 68 | 15 | 0 |
| Minimal Container Images | 79 | 0.1% | 58 | 21 | 0 |
| Code Efficiency & Lean Code | 79 | 0.1% | 78 | 1 | 0 |
| Minify Web Assets | 72 | 0.1% | 71 | 1 | 0 |
| Algorithm Optimization | 71 | 0.1% | 70 | 1 | 0 |
| Pre-trained Transfer Learning | 64 | 0.1% | 53 | 11 | 0 |
| Infrastructure as Code Optimization | 61 | 0.1% | 45 | 16 | 0 |
| Optimize Images | 59 | 0.1% | 59 | 0 | 0 |
| Pod Disruption Budget | 57 | 0.1% | 46 | 11 | 0 |
| Energy-Aware Monitoring | 54 | 0.1% | 41 | 13 | 0 |
| Compress ML Models for Inference | 51 | 0.1% | 51 | 0 | 0 |
| Use DDoS Protection | 49 | 0.1% | 38 | 11 | 0 |
| Rate Limiting | 46 | 0.1% | 46 | 0 | 0 |
| Pagination & Lazy Loading | 45 | 0.1% | 38 | 7 | 0 |
| Reactive Streams | 43 | 0.1% | 33 | 10 | 0 |
| Model Pruning | 35 | 0.1% | 34 | 1 | 0 |
| Application Performance Monitoring | 31 | 0.1% | 28 | 3 | 0 |
| GraphQL for Selective Retrieval | 29 | 0.1% | 20 | 9 | 0 |
| Circuit Breaker & Bulkhead | 27 | 0.0% | 23 | 4 | 0 |
| Service Mesh Optimization | 27 | 0.0% | 23 | 4 | 0 |
| Reduce Reflection Usage | 24 | 0.0% | 21 | 3 | 0 |
| Energy Efficient AI at Edge | 24 | 0.0% | 24 | 0 | 0 |
| Graceful Shutdown | 19 | 0.0% | 18 | 1 | 0 |
| Early Stopping | 19 | 0.0% | 17 | 2 | 0 |
| Service Decomposition & Right-Sizing | 18 | 0.0% | 16 | 2 | 0 |
| Service Co-location | 16 | 0.0% | 12 | 4 | 0 |
| Memoization | 16 | 0.0% | 15 | 1 | 0 |
| Batch Inference Optimization | 14 | 0.0% | 14 | 0 | 0 |
| Query Optimization | 13 | 0.0% | 12 | 1 | 0 |
| Edge Inference | 12 | 0.0% | 12 | 0 | 0 |
| Resource Pooling | 12 | 0.0% | 12 | 0 | 0 |
| Garbage Collection Tuning | 9 | 0.0% | 9 | 0 | 0 |
| Multi-Level Caching | 7 | 0.0% | 7 | 0 | 0 |
| Dynamic Resource Allocation | 7 | 0.0% | 4 | 3 | 0 |
| Batch Inference | 6 | 0.0% | 6 | 0 | 0 |
| Request Batching & Aggregation | 6 | 0.0% | 5 | 1 | 0 |
| Knowledge Distillation | 6 | 0.0% | 6 | 0 | 0 |
| Precomputation & Pre-aggregation | 5 | 0.0% | 5 | 0 | 0 |
| Keep-Alive Connections | 2 | 0.0% | 1 | 1 | 0 |
| Prepared Statements | 2 | 0.0% | 2 | 0 | 0 |
| Right-size Resources | 2 | 0.0% | 2 | 0 | 0 |
| Renewable Energy Regions | 1 | 0.0% | 1 | 0 | 0 |


**Detailed Pattern Analysis:**

**1. Keep Request Counts Low**
- Frequency: 4,281 commits (7.4%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: a1d638ea, 7a4d6501, c8f8bb83
**2. Use Compiled Languages**
- Frequency: 3,715 commits (6.4%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: 498896ec, 57b65a25, 7a4d6501
**3. Delete Unused Storage Resources**
- Frequency: 3,493 commits (6.0%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: 9c7a83d3, 57b65a25, 7a4d6501
**4. Remove Unused Assets**
- Frequency: 3,000 commits (5.2%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: 9c7a83d3, 57b65a25, 7a4d6501
**5. Use Serverless**
- Frequency: 1,934 commits (3.3%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: 2a4951be, 7a4d6501, 66d4bd32
**6. Minimize Deployed Environments**
- Frequency: 1,902 commits (3.3%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: cd7d35fa, ecf7e6d4, 7a4d6501
**7. Reduce Transmitted Data**
- Frequency: 1,776 commits (3.1%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: f758d085, 66d4bd32, db841afd
**8. Serve Images in Modern Formats**
- Frequency: 1,630 commits (2.8%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: a1d638ea, 7a4d6501, ad012f63
**9. Resource Limits & Constraints**
- Frequency: 1,427 commits (2.5%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: dfa6aa22, ad012f63, 41c598c4
**10. Containerize Your Workload**
- Frequency: 1,412 commits (2.4%)
- Confidence Distribution: HIGH=1, MEDIUM=0, LOW=0
- Example Commits: 1ff74821, 9c7a83d3, 7a4d6501

#### 2.3 Emerging Practices Discovered

No novel microservice-specific green practices were automatically detected. Manual review of high-impact commits may reveal emerging patterns not captured by keyword matching.

#### 2.4 Per-Repository Analysis

**Top 10 Greenest Repositories (by % green-aware commits):**

| Repository | Total Commits | Green Commits | Percentage | Patterns Detected |
|------------|---------------|---------------|------------|-------------------|
| moby/moby | 500 | 487 | 97.4% | Choose Region Closest to Users, Defer Offscreen Images, Optimize Storage Resource Utilization |
| pingcap/tidb | 500 | 478 | 95.6% | Optimize Storage Resource Utilization, Choose Region Closest to Users, Efficient Format for Model Training |
| webyog/sqlyog-community | 132 | 118 | 89.4% | Scale Infrastructure with User Load, Efficient Format for Model Training, Scale Down Unused Applications |
| paiml/depyler | 500 | 445 | 89.0% | Choose Region Closest to Users, Efficient Format for Model Training, Batch Inference |
| cockroachdb/cockroach | 500 | 426 | 85.2% | Choose Region Closest to Users, Efficient Format for Model Training, Pagination & Lazy Loading |
| sustainable-computing-io/kepler | 299 | 252 | 84.3% | Optimize Storage Resource Utilization, Defer Offscreen Images, Use Cloud Native Security Tools |
| milvus-io/milvus | 500 | 405 | 81.0% | Choose Region Closest to Users, Efficient Format for Model Training, Reactive Streams |
| envoyproxy/envoy | 500 | 381 | 76.2% | Choose Region Closest to Users, Efficient Format for Model Training, Pagination & Lazy Loading |
| Stirling-Tools/Stirling-PDF | 500 | 367 | 73.4% | Choose Region Closest to Users, Efficient Format for Model Training, Reactive Streams |
| openfaas/faas | 500 | 365 | 73.0% | Optimize Storage Resource Utilization, Defer Offscreen Images, Choose Region Closest to Users |


**Repositories with No Green Mentions:** 2 out of 100 repositories had zero green-aware commits.

#### 2.5 Enhanced Statistical Analysis

This section presents advanced statistical analyses of green software engineering patterns.

##### Temporal Trends

##### Effect Size Analysis

##### Descriptive Statistics


### 3. Discussion

#### 3.1 Interpretation of Findings

The analysis reveals that 46.0% of microservice commits explicitly address energy efficiency or sustainability concerns. This high percentage suggests that:

1. **Green software practices exist but are not mainstream:** While developers are applying some energy-efficient patterns, sustainability is not yet a primary concern in microservices development.

2. **Implicit vs. Explicit practices:** Many optimizations (e.g., caching, async processing) may improve energy efficiency without explicitly mentioning it in commit messages.

3. **Domain-specific awareness:** Some repositories show significantly higher green awareness, suggesting that certain domains (e.g., cloud-native, high-scale systems) are more conscious of resource efficiency.

#### 3.2 How Microservice Developers Approach Energy Efficiency

Based on the detected patterns, microservice developers primarily focus on:

- **Performance optimization** as a proxy for energy efficiency
- **Caching strategies** to reduce redundant computations
- **Resource pooling** to minimize connection overhead
- **Asynchronous processing** to improve resource utilization

#### 3.3 Gap Analysis: Literature vs. Practice

**Literature Emphasis:**
- Formal green software engineering methodologies
- Energy measurement and profiling
- Carbon-aware computing

**Practice Emphasis:**
- Performance optimization (implicitly green)
- Cost reduction (aligned with energy efficiency)
- Scalability patterns (may or may not be green)

**Gap:** Explicit sustainability terminology is rare in commit messages, even when applying green patterns.

#### 3.4 Implications for Green Software Engineering in Distributed Systems

1. **Need for awareness:** Developers would benefit from education on how common optimizations contribute to sustainability
2. **Tooling opportunity:** IDE plugins or CI/CD checks could highlight energy implications of code changes
3. **Metrics integration:** Including energy/carbon metrics alongside performance metrics in monitoring dashboards
4. **Best practices dissemination:** Green microservices patterns should be documented and promoted in the community

### 4. Limitations

#### 4.1 Sample Size and Selection Bias

- Analysis limited to top-starred repositories, which may not represent typical microservices projects
- GitHub-centric sample excludes private enterprise repositories
- Selection based on keywords may miss relevant projects with different terminology

#### 4.2 Commit Message Analysis Limitations

- Commit messages may not fully describe code changes
- Keyword matching cannot detect implicit green practices in code
- English-only analysis excludes international projects
- Developers may not document energy implications in commit messages

#### 4.3 Scope Limitations

- 2-year time window may not capture long-term trends
- Focus on microservices excludes monolithic and other architectures
- No code-level analysis (only commit metadata)
- Heuristic classification may have false positives/negatives

#### 4.4 Future Work Suggestions

1. **AI-powered analysis:** Use Claude Sonnet or similar LLMs for deeper semantic understanding
2. **Code-level inspection:** Analyze actual code changes, not just commit messages
3. **Longitudinal study:** Track green practices evolution over time
4. **Developer surveys:** Complement automated analysis with developer perspectives
5. **Energy measurement:** Correlate detected patterns with actual energy consumption data

### 5. Conclusion

#### 5.1 Summary of Key Findings

This study analyzed 39,664 commits from 100 microservice repositories and found:

1. **46.0%** of commits explicitly address energy/sustainability concerns
2. **98** repositories demonstrate some level of green awareness
3. Common green patterns include: Keep Request Counts Low, Use Compiled Languages, Delete Unused Storage Resources

#### 5.2 Answers to Research Questions

**RQ1: What percentage of microservice commits explicitly mention energy efficiency?**
Answer: 46.0% of analyzed commits contain explicit mentions.

**RQ2: Which green software tactics are developers applying in practice?**
Answer: Developers primarily apply caching strategies, resource pooling, database optimization, and asynchronous processing patterns.

**RQ3: Are there novel microservice-specific green practices not yet documented?**
Answer: Automated keyword analysis found limited evidence of novel patterns. Manual review and AI-powered analysis may reveal more nuanced practices.

#### 5.3 Recommendations for Practitioners

1. **Adopt explicit green terminology:** Document energy implications in commit messages and PR descriptions
2. **Measure and monitor:** Integrate energy/carbon metrics into observability platforms
3. **Apply known patterns:** Systematically apply caching, pooling, and optimization patterns with sustainability in mind
4. **Education and training:** Incorporate green software engineering principles into team training

#### 5.4 Recommendations for Researchers

1. **Develop better detection tools:** Create AI-powered tools for identifying green practices in code
2. **Build pattern catalogs:** Document microservice-specific green patterns with examples
3. **Conduct empirical studies:** Measure actual energy savings from detected patterns
4. **Create benchmarks:** Establish baseline metrics for green microservices

---

**Report End**

*For questions or additional analysis, please refer to the accompanying data files: `green_analysis_results.csv` and `aggregated_statistics.json`*