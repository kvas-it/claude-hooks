#!/usr/bin/env python3
"""Claude Code notification hook that shows macOS notifications."""

import argparse
import json
import os
import subprocess
import sys


def get_terminal_app():
    """Try to detect which terminal application is running."""
    try:
        ppid = os.getppid()
        result = subprocess.run(
            ["ps", "-p", str(ppid), "-o", "comm="], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            process_name = result.stdout.strip()
            terminal_map = {
                "alacritty": "org.alacritty",
                "iterm": "com.googlecode.iterm2",
                "iterm2": "com.googlecode.iterm2", 
                "terminal": "com.apple.Terminal",
                "kitty": "net.kovidgoyal.kitty",
                "wezterm": "com.github.wez.wezterm"
            }
            
            for term_name, bundle_id in terminal_map.items():
                if term_name in process_name.lower():
                    return bundle_id
    except Exception:
        pass
    
    return "org.alacritty"


def show_notification(title, text):
    """Show a macOS notification using terminal-notifier or osascript."""
    terminal_bundle_id = get_terminal_app()
    
    try:
        subprocess.run([
            "terminal-notifier", 
            "-title", title,
            "-message", text,
            "-sound", "default",
            "-activate", terminal_bundle_id
        ], check=True)
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Escape quotes to prevent AppleScript injection
    title = title.replace('"', '\\"')
    text = text.replace('"', '\\"')
    
    cmd = f'osascript -e \'display notification "{text}" with title "{title}" sound name "default"\''
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to show notification: {e}", file=sys.stderr)


def main():
    """Main entry point for the notification hook."""
    parser = argparse.ArgumentParser(description="Show macOS notifications for Claude Code")
    parser.add_argument("--title", help="Custom notification title")
    parser.add_argument("--message", help="Custom notification message")
    args = parser.parse_args()
    
    if args.title and args.message:
        show_notification(args.title, args.message)
        return
    
    try:
        input_data = sys.stdin.read().strip()
        
        if input_data:
            data = json.loads(input_data)
            tool = data.get("tool", "Unknown")
            command = data.get("command", "")
            status = data.get("status", "")
            
            title = args.title or f"Claude Code: {tool}"
            
            if args.message:
                text = args.message
            else:
                text_parts = []
                if command:
                    if len(command) > 50:
                        command = command[:47] + "..."
                    text_parts.append(f"Command: {command}")
                
                if status:
                    text_parts.append(f"Status: {status}")
                
                if not text_parts:
                    text_parts.append("Hook executed")
                
                text = " | ".join(text_parts)
        else:
            title = args.title or "Claude Code"
            text = args.message or "Hook executed"
        
        show_notification(title, text)
        
    except json.JSONDecodeError as e:
        title = args.title or "Claude Code Hook"
        text = args.message or f"JSON parse error: {e}"
        show_notification(title, text)
    except Exception as e:
        title = args.title or "Claude Code Hook"
        text = args.message or f"Error: {e}"
        show_notification(title, text)


if __name__ == "__main__":
    main()