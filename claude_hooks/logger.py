#!/usr/bin/env python3
"""Claude Code logging hook that writes events to a JSONL file."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    """Main entry point for the logging hook."""
    parser = argparse.ArgumentParser(description="Log Claude Code hook data to a JSONL file")
    parser.add_argument("log_file", help="Path to the log file")
    args = parser.parse_args()
    
    log_file = Path(args.log_file)
    
    # Create parent directory if it doesn't exist
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Read all input from stdin
    input_data = sys.stdin.read().strip()
    
    # Parse input as JSON
    try:
        log_entry = json.loads(input_data)
        # Add timestamp to the parsed object
        log_entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    except json.JSONDecodeError as e:
        # If parsing fails, create an error log entry
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": f"Failed to parse JSON: {e}",
            "raw_input": input_data
        }
    
    # Append to JSONL file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    print(f"Logged to {log_file}")


if __name__ == "__main__":
    main()