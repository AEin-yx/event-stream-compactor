## Day 0 Task 0: Project Initialized  
Basic repo setup and structure

---
## Day 1 Task 1: Core Logging Tools
### Technical Achievements
- Implemented Typer-based CLI framework
- Created three specialized logging commands
- Established consistent error handling pattern

### System Design Decisions
- Chose Typer for CLI: Modern Python framework with strong type support
- Selected deque for logtail: Memory-efficient circular buffer
- Implemented UTF-8 with error replacement: Robust character handling

### Performance Considerations
- Memory usage optimization in logtail
- File reading efficiency tradeoffs
- Regex pattern matching performance

### Learning Outcomes
- Understanding of memory vs speed tradeoffs
- Experience with file encoding challenges
- Insight into statistics validation

### Future Enhancements
- Add streaming support for large files
- Implement configurable encodings
- Develop comprehensive test suite

## Day 2 Task 2: Log Parser Engine
### Technical Achievements
- Implemented regex-based HDFS log parser with ISO-8601 timestamp conversion
- Developed statistical analysis module (events/sec, log level distribution)
- Created structured JSON output for downstream compaction
- Built fault-tolerant parsing (invalid timestamp handling)

### System Design Decisions
- **Chose regex over NLP**: Chose regex for pattern matching: Flexible and efficient
- **ISO timestamps**: Prioritized sortable format for time-based compaction
- Added statistics calculation: Provides log distribution insights
- **Dynamic field handling**: Preserved raw message while extracting components

### Performance Considerations
- File reading efficiency
- Memory usage optimization
- Timestamp processing overhead
- Statistics calculation impact

### Learning Outcomes
- Understanding of log format parsing
- Experience with timestamp handling
- Statistical patterns in operational logs (96% INFO = low compaction priority)
- Knowledge of error handling patterns

### Future Enhancements
- Add streaming support
- Implement configurable formats
- Develop comprehensive testing
- Add filtering capabilities
- Sampling mode for billion-scale logs

## Day 3 Task 3: In-Memory Key-Value Store (Mini-Redis Clone)
### Technical Achievements

- Implemented full CRUD operations (SET, GET, DELETE) with TTL support  
- Built cross-platform file persistence with atomic writes and JSON serialization  
- Created Typer-based CLI with proper argument handling and user feedback  
- Developed TTL-based expiration system with lazy cleanup on key access  
- Added statistics tracking (total keys, TTL keys) and administrative commands  

### System Design Decisions

- Write-through cache pattern: Chose immediate disk persistence for consistency and crash safety over batched writes  
- Lazy TTL cleanup: Expired keys removed on access rather than background scanning - scales with actual usage  
- JSON persistence: Selected human-readable format over binary for debugging and learning transparency  
- Cross-platform atomic writes: Handled Windows/Unix file replacement differences for data integrity  
- CLI process isolation: Each command runs as separate process, requiring disk persistence between invocations  

### Critical Design Insights & Tradeoffs

- Lazy vs Eager vs Hybrid cleanup strategies: Discovered that different TTL patterns need different approaches  
- Short TTLs benefit from lazy cleanup (immediate removal on access)  
- Long TTLs benefit from periodic batch cleanup  
- Hybrid approach adapts to usage patterns dynamically  
- Memory vs Disk consistency: Learned importance of keeping in-memory state synchronized with persistent storage   
- Write-through vs Write-back: Prioritized consistency over performance for learning - easily evolvable to batched writes for production

### Performance Considerations

- Disk I/O on every operation (acceptable for learning, optimizable via batching)  
- JSON parsing overhead vs binary formats  
- File locking and atomic write operations  
- TTL cleanup computational cost vs memory bloat  

### Learning Outcomes

- Systems thinking development: Understanding of fundamental cache patterns used across distributed systems
- Data consistency patterns: Experience with keeping multiple storage layers synchronized
- Operational tradeoffs: Real-world understanding of durability vs throughput decisions
- Error handling: Cross-platform file operations and graceful failure modes
- CLI design patterns: Building user-friendly command interfaces with proper feedback

### Connection to Event Stream Compaction

- TTL patterns directly apply to log retention policies
- Cleanup strategies map to compaction triggers (time-based vs size-based vs access-based)
- Memory/disk consistency crucial for log segment management
- Write-through pattern applicable to immediate log durability requirements

### Future Enhancements

- Add batching/async writes for throughput optimization  
- Implement background TTL cleanup thread  
- Add data compression and binary serialization  
- Create network protocol for true Redis compatibility  
- Add memory usage monitoring and eviction policies  
- Implement clustering and replication patterns  

### Key Debugging Moments
- Process isolation discovery: Each CLI command creates new process, requiring disk persistence
- Atomic write platform differences: Windows vs Unix file replacement behavior
- Cleanup consistency: Expired keys cleaned from memory but persisted to disk until fixed

## Day 4
Design Review & Strategic De-prioritization (Rate Limiting)  
Goal: Conducted an in-depth design review of potential components, specifically assessing the role and necessity of rate limiting within the core Event Stream Compactor architecture.

### Technical Achievements (Without implementation):  

Researched and understood various rate limiting algorithms (Token Bucket, Leaky Bucket, Sliding Window Log/Counter).  
Analyzed the typical input/output and use cases for rate limiters in distributed systems.  
Evaluated the trade-offs associated with different rate limiting strategies (e.g., memory vs. accuracy, consistency in distributed environments).  
### System Design Decisions:

- Decision to De-prioritize Rate Limiter Implementation for Core Project Scope: After thorough review and alignment with the primary goal of demonstrating a "Distributed Event Stream Compactor," it was decided that a dedicated rate limiter component, while a valuable general distributed systems pattern, is not critical to the core value proposition and functionality of this specific project.
- The primary objective of this project is to showcase end-to-end event stream compaction and distributed storage/aggregation.
Rate limiting primarily controls the ingestion rate or resource access rate to a system, preventing overload. While important for a production system, it's a distinct concern from the compaction logic itself and the efficient storage of compacted data.
- Implementing a robust, production-grade rate limiter (especially one that accounts for distribution and consistency) would introduce significant complexity and time commitment, diverting resources from the core compaction and distribution mechanisms that are the project's unique point.
- The project's current focus is on demonstrating the pipeline from raw logs to compacted, aggregated streams, where performance is handled via buffering (Producer-Consumer) and efficient algorithms (Stream Compressor).