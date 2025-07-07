#!/usr/bin/env python3
"""Claude Code ruff hook for linting and formatting Python files."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def is_python_file(file_path):
    """Check if a file is a Python file."""
    path = Path(file_path)
    return path.suffix == '.py'


def run_ruff(files, mode="check"):
    """Run ruff on the specified files."""
    if not files:
        print("No Python files to process")
        return True
    
    # Check if ruff is available
    try:
        subprocess.run(["ruff", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ruff is not installed. Install with: pip install ruff", file=sys.stderr)
        return False
    
    # Filter for Python files only
    python_files = [f for f in files if is_python_file(f)]
    if not python_files:
        print("No Python files found to process")
        return True
    
    # Build ruff command
    cmd = ["ruff"]
    if mode == "check":
        cmd.append("check")
    elif mode == "fix":
        cmd.extend(["check", "--fix"])
    else:
        print(f"Error: Unknown mode '{mode}'. Use 'check' or 'fix'", file=sys.stderr)
        return False
    
    cmd.extend(python_files)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print stdout if there's any output
        if result.stdout:
            print(result.stdout)
        
        # Print stderr if there's any error output
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print(f"✓ ruff {mode} completed successfully on {len(python_files)} file(s)")
            return True
        else:
            print(f"✗ ruff {mode} found issues in {len(python_files)} file(s)")
            return False
            
    except Exception as e:
        print(f"Error running ruff: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for the ruff hook."""
    parser = argparse.ArgumentParser(description="Run ruff on Python files from Claude Code")
    parser.add_argument("--check", action="store_true", help="Check files for issues (default)")
    parser.add_argument("--fix", action="store_true", help="Fix issues automatically")
    args = parser.parse_args()
    
    # Determine mode
    if args.fix:
        mode = "fix"
    else:
        mode = "check"  # Default to check mode
    
    try:
        # Read JSON data from stdin
        input_data = sys.stdin.read().strip()
        
        if not input_data:
            print("No input data provided", file=sys.stderr)
            sys.exit(1)
        
        # Parse JSON
        data = json.loads(input_data)
        
        # Extract file paths - support various JSON structures
        files = []
        if isinstance(data, dict):
            # Handle {"files": ["file1.py", "file2.py"]}
            if "files" in data:
                files = data["files"]
            # Handle {"file": "single_file.py"}
            elif "file" in data:
                files = [data["file"]]
            # Handle {"file_path": "single_file.py"} (common in hooks)
            elif "file_path" in data:
                files = [data["file_path"]]
        elif isinstance(data, list):
            # Handle direct list of files
            files = data
        
        if not files:
            print("No files found in input data", file=sys.stderr)
            sys.exit(1)
        
        # Run ruff
        success = run_ruff(files, mode)
        sys.exit(0 if success else 1)
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()