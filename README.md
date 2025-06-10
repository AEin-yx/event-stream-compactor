# event-stream-compactor 
## Project Overview  
The Event Stream Compactor is a robust, modular system designed to process, analyze, and efficiently store high-volume event streams, akin to log compaction in distributed systems. This project demonstrates core principles of data engineering, distributed systems, and efficient data handling by implementing a pipeline for raw log ingestion, parsing, statistical analysis, and persistent storage.

## How to Run ?
Clone the Repo: `https://github.com/AEin-yx/event-stream-compactor.git`  
`cd event-stream-compactor`  

For Requirements: `pip install -r requirements.txt`  
## Key Features & Technical Achievements
This project is built around several interconnected modules, each addressing a critical aspect of event stream processing:  
### CLI Framework  
- Typer-based CLI : Used typer for command line interface  
- Logging Commands:  
`logread` : `python main.py logread <path_to_log_file>`   
`loggrep` : `python main.py loggrep <path_to_log_file> <pattern> --stats`  
`logtail` : `python main.py logtail <path_to_log_file> <some number like 20>`  
- Memory-Efficient logtail: Utilized a deque (double-ended queue) for optimized memory usage when tailing large log files.
### Log Parser Engine  
- Regex-based HDFS Log Parser: Engineered a highly efficient parser for HDFS logs, including automatic ISO-8601 timestamp conversion for standardized data representation
- Statistical Analysis Module: Developed capabilities to extract key metrics from log streams, such as events per second and log level distribution, providing immediate operational insights.
- Fault-Tolerant Parsing: Implemented robust error handling for invalid timestamps and malformed log entries, ensuring continuous processing.
- Run the parser engine with `python parser.py logs\raw\HDFS_2k.log --stats`
### In Memory key value store(mini redis clone)  
- Full CRUD Operations with TTL: Implemented core SET, GET, DELETE operations with support for Time-To-Live (TTL), enabling automatic expiration of data.
- Comprehensive Statistics & Admin Commands: Tracked total and TTL-managed keys, along with administrative commands for system oversight.
- Commands:  
`set` : `python kvstore_cli.py set <key> <value> --ttl <some_number in sec like 60>`(set a key value pair)  
`get` : `python kvstore_cli.py get <key>`(get value using a key)  
`delete` : `python kvstore_cli.py delete <key>`(delete a key)  
`stats` : `python kvstore_cli.py stats`(keys state in store)  
`clear` : `python kvstore_cli.py clear`(reset whole store)  
`store` : `python kvstore_cli.py store`(prints all keys values present in both ttl and cache)  

## Project Structure

```
EVENT-STREAM-COMPACTOR/
├── docs/
│   └── progress.md               # Detailed daily progress logs
├── kv_store/
│   ├── kvstore_cli.py            # CLI for the Key-Value Store
│   └── kvstore.py                # Core Key-Value Store implementation
├── logs/
│   └── raw/
│       ├── HDFS_2k.log           # Sample HDFS log file
│       └── HDFS_synthetic.log    # Another sample HDFS log file
├── .gitignore                    # Git ignore file
├── kvstore.json                  # Persistent storage for the Key-Value Store
├── main.py                       # CLI and its logic
├── parser.py                     # Log parsing logic
└── README.md                     # Project README (this file)
└── requirements.txt              # Include necessary packages used in the project
```