# Claude Hooks

Python hooks for [Claude Code](https://claude.ai/code) that provide logging and notification functionality. This is a rather quick and dirty implementation for my needs, that is a work in progress, but you're welcome to use it.

## Features

- **claude-logger**: Logs Claude Code hook data to JSONL files with timestamps
- **claude-notify**: Shows macOS notifications with smart terminal activation

## Installation

```bash
pip install -e .
```

## Usage

### Logging Hook

```bash
claude-logger /path/to/log/file.jsonl
```

### Notification Hook

```bash
# Custom notification
claude-notify --title "Title" --message "Message"

# Parse JSON from stdin
echo '{"tool": "bash", "command": "ls"}' | claude-notify
```

## Claude Code Integration

Configure in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "claude-notify --title 'Claude Code' --message 'Notification received'"
          }
        ]
      }
    ]
  }
}
```

## Requirements

- Python 3.10+
- macOS (for notifications)
- Optional: `terminal-notifier` for enhanced notifications
