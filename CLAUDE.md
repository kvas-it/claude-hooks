# Claude Hooks

This repository contains Python scripts designed to work as hooks for Claude Code. Each script is packaged as a console command that becomes available system-wide after installation.

## Installation

```bash
pip install -e .
```

## Available Hooks

### `claude-logger`
Logs Claude Code hook data to JSONL files with timestamps.

**Usage:**
```bash
claude-logger /path/to/log/file.jsonl
```

**Features:**
- Parses JSON input from stdin
- Adds timestamp to the parsed object
- Writes enhanced JSON to specified log file
- Creates parent directories if they don't exist
- Handles JSON parsing errors gracefully

### `claude-notify`
Shows macOS notifications with sound and smart terminal activation.

**Usage:**
```bash
# Custom notification
claude-notify --title "Title" --message "Message"

# Parse JSON from stdin
echo '{"tool": "bash", "command": "ls"}' | claude-notify

# Mixed mode (custom title + JSON data)
echo '{"tool": "bash"}' | claude-notify --title "Custom Title"
```

**Features:**
- Detects which terminal application is running (Alacritty, iTerm2, Terminal, etc.)
- Uses `terminal-notifier` when available for better click behavior
- Falls back to `osascript` for notifications
- Plays notification sound
- Clicking notification activates the correct terminal

## Global Hook Configuration

The hooks are configured in `~/.claude/settings.json` for global Claude Code integration:

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
    ],
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "claude-notify --title 'Claude Code' --message 'Input required'"
          }
        ]
      }
    ]
  }
}
```

## Package Structure

```
claude-hooks/
├── pyproject.toml          # Package configuration
├── README.md              # Project documentation
├── CLAUDE.md              # This file
├── claude_hooks/
│   ├── __init__.py        # Package initialization
│   ├── logger.py          # JSONL logging hook
│   └── notifier.py        # macOS notification hook
```

## Development

The package uses editable installation (`pip install -e .`) which allows you to modify the scripts and see changes immediately without reinstalling.

## Dependencies

- **Runtime**: No external dependencies (uses only Python standard library)
- **macOS notifications**: Uses `terminal-notifier` if available, falls back to `osascript`
- **Terminal detection**: Uses `ps` command to detect parent process