#!/usr/bin/env python3
"""
auto-adapt-mode: Learn from user's tool approvals and update Claude config.

Hook Type: PostToolUse
Event: Fires after a tool is successfully executed (meaning user approved it)

Behavior:
- When user approves a tool/command, generalize it into a permission rule
- Add the generalized rule to ~/.claude/settings.json permissions.allow
- NEVER remember dangerous/destructive commands (rm -rf, force-push, DROP, etc.)
- On first run, seeds the config with auto-mode-equivalent baseline permissions

Usage in settings.json:
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/06-hooks/auto-adapt-mode.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
"""

import json
import os
import sys
import re
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"
LOG_PATH = Path.home() / ".claude" / "auto-adapt-mode.log"

# Auto-mode baseline permissions (equivalent to Claude Code's auto-mode defaults)
# These are safe, local, reversible operations that auto-mode allows without prompting
AUTO_MODE_BASELINE = [
    # File operations (read/write in working directory)
    "Read(*)",
    "Edit(*)",
    "Write(*)",
    "Glob(*)",
    "Grep(*)",
    # Git read operations
    "Bash(git status:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git branch:*)",
    "Bash(git show:*)",
    "Bash(git rev-parse:*)",
    "Bash(git remote -v:*)",
    "Bash(git fetch:*)",
    "Bash(git stash list:*)",
    # Git write operations (local, reversible)
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git checkout:*)",
    "Bash(git switch:*)",
    "Bash(git merge:*)",
    "Bash(git rebase:*)",
    "Bash(git stash:*)",
    "Bash(git tag:*)",
    "Bash(git worktree:*)",
    # Package managers (install from manifests)
    "Bash(npm install:*)",
    "Bash(npm ci:*)",
    "Bash(npm test:*)",
    "Bash(npm run:*)",
    "Bash(npx:*)",
    "Bash(pip install:*)",
    "Bash(pip3 install:*)",
    "Bash(cargo build:*)",
    "Bash(cargo test:*)",
    "Bash(go build:*)",
    "Bash(go test:*)",
    "Bash(go mod:*)",
    # Build and test
    "Bash(make:*)",
    "Bash(cmake:*)",
    "Bash(pytest:*)",
    "Bash(python3 -m pytest:*)",
    # Common safe commands
    "Bash(ls:*)",
    "Bash(pwd:*)",
    "Bash(which:*)",
    "Bash(echo:*)",
    "Bash(cat:*)",
    "Bash(head:*)",
    "Bash(tail:*)",
    "Bash(wc:*)",
    "Bash(sort:*)",
    "Bash(uniq:*)",
    "Bash(find:*)",
    "Bash(dirname:*)",
    "Bash(basename:*)",
    "Bash(realpath:*)",
    "Bash(mkdir:*)",
    "Bash(touch:*)",
    "Bash(cp:*)",
    "Bash(mv:*)",
    "Bash(chmod:*)",
    "Bash(date:*)",
    "Bash(env:*)",
    "Bash(printenv:*)",
    # File inspection
    "Bash(file:*)",
    "Bash(stat:*)",
    "Bash(diff:*)",
    "Bash(md5sum:*)",
    "Bash(sha256sum:*)",
    # GitHub CLI (read operations)
    "Bash(gh pr view:*)",
    "Bash(gh pr list:*)",
    "Bash(gh issue view:*)",
    "Bash(gh issue list:*)",
    "Bash(gh repo view:*)",
    # Agents and tools
    "Agent(*)",
    "Skill(*)",
    "WebSearch(*)",
    "WebFetch(*)",
    "NotebookEdit(*)",
    "TaskCreate(*)",
    "TaskUpdate(*)",
]

# ──────────────────────────────────────────────────────────────────────────────
# Dangerous patterns: commands/tools that should NEVER be auto-remembered
# These are irreversible, destructive, or affect shared/production systems
# ──────────────────────────────────────────────────────────────────────────────

DANGEROUS_PATTERNS = [
    # Destructive file operations
    r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*|--recursive)",  # rm -rf, rm -r
    r"rm\s+(-[a-zA-Z]*f[a-zA-Z]*)",               # rm -f (force delete)
    r"rmdir",
    r"shred\b",
    r"dd\s+if=",                                    # disk overwrite
    r"mkfs\b",                                      # format filesystem
    r"format\b",

    # Git destructive operations
    r"git\s+push\s+(-[a-zA-Z]*f|--force)",          # force push
    r"git\s+push\s+--force-with-lease",
    r"git\s+reset\s+--hard",                         # hard reset
    r"git\s+clean\s+(-[a-zA-Z]*f|--force)",          # clean force
    r"git\s+checkout\s+\.",                           # discard all changes
    r"git\s+restore\s+\.",
    r"git\s+branch\s+(-[a-zA-Z]*D|-d\s+main|-d\s+master)",  # delete branches
    r"git\s+push\s+.*:.*main",                       # delete remote main
    r"git\s+push\s+.*:.*master",

    # Database destructive operations
    r"DROP\s+(TABLE|DATABASE|SCHEMA|INDEX)",
    r"TRUNCATE\b",
    r"DELETE\s+FROM\s+(?!.*WHERE)",                  # DELETE without WHERE
    r"ALTER\s+TABLE\s+.*DROP",

    # System-level dangerous operations
    r"sudo\b",
    r"chmod\s+777",
    r"chown\s+-R\s+root",

    # Network exfiltration / remote execution
    r"curl\s+.*\|\s*(bash|sh|zsh)",                  # pipe to shell
    r"wget\s+.*\|\s*(bash|sh|zsh)",
    r"curl\s+.*--upload-file",
    r"curl\s+.*-T\s+",                               # upload
    r"scp\b(?!.*localhost)",                          # remote copy (not local)
    r"rsync\b.*[^/]:",                                # remote rsync

    # Container/infra destructive
    r"docker\s+(rm|rmi|system\s+prune)",
    r"kubectl\s+delete",
    r"terraform\s+destroy",

    # Package publishing (irreversible)
    r"npm\s+publish",
    r"pip\s+upload",
    r"cargo\s+publish",

    # Environment/secret exposure
    r"printenv\s+.*SECRET",
    r"printenv\s+.*PASSWORD",
    r"printenv\s+.*TOKEN",
    r"echo\s+\$.*SECRET",
    r"echo\s+\$.*PASSWORD",

    # Process killing
    r"kill\s+-9",
    r"killall\b",
    r"pkill\b",

    # Production deployment
    r"deploy\s+.*prod",
    r"migrate\s+.*prod",
]

# Tools that should never be auto-allowed (non-Bash)
DANGEROUS_TOOLS = {
    "Bash",  # Generic Bash(*) wildcard is dangerous — we allow specific commands only
}


# ──────────────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────────────

def log(message: str):
    """Append a log entry for debugging."""
    try:
        with open(LOG_PATH, "a") as f:
            from datetime import datetime
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
    except Exception:
        pass


def is_dangerous_command(command: str) -> bool:
    """Check if a bash command matches any dangerous pattern."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


def generalize_tool_permission(tool_name: str, tool_input: dict) -> str | None:
    """
    Convert a specific tool invocation into a generalized permission rule.

    Returns None if the tool/command should not be remembered.
    """
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if not command:
            return None

        # Never remember dangerous commands
        if is_dangerous_command(command):
            log(f"BLOCKED dangerous: {command}")
            return None

        # Extract the base command (first word or first two words for git/npm/etc.)
        parts = command.strip().split()
        if not parts:
            return None

        base = parts[0]

        # For compound commands (git push, npm run, gh pr create, etc.)
        # generalize to "base subcommand:*"
        compound_prefixes = [
            "git", "npm", "npx", "pip", "pip3", "cargo", "go",
            "docker", "kubectl", "gh", "python3", "python", "node",
            "make", "cmake", "pytest", "ruby", "java", "javac",
        ]

        if base in compound_prefixes and len(parts) > 1:
            sub = parts[1]
            # Don't generalize dangerous subcommands even if pattern didn't catch them
            danger_subs = {"rm", "delete", "destroy", "prune", "publish"}
            if sub.lower() in danger_subs:
                log(f"BLOCKED dangerous sub: {base} {sub}")
                return None
            return f"Bash({base} {sub}:*)"

        # For simple commands, generalize with wildcard args
        return f"Bash({base}:*)"

    elif tool_name in DANGEROUS_TOOLS:
        return None

    else:
        # Non-Bash tools: allow with wildcard
        # These are Claude Code built-in tools (Read, Write, Edit, etc.)
        # Most are already in the baseline, but learn new ones
        return f"{tool_name}(*)"


def load_settings() -> dict:
    """Load the current settings.json."""
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    return {}


def save_settings(settings: dict):
    """Save settings.json with formatting."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")


def ensure_baseline(settings: dict) -> bool:
    """
    Ensure auto-mode baseline permissions are seeded into settings.
    Returns True if any changes were made.
    """
    permissions = settings.setdefault("permissions", {})
    allow = permissions.setdefault("allow", [])

    # Track what's already there (normalized for comparison)
    existing = set(allow)
    added = []

    for rule in AUTO_MODE_BASELINE:
        if rule not in existing:
            allow.append(rule)
            existing.add(rule)
            added.append(rule)

    if added:
        log(f"Seeded {len(added)} baseline rules")
        return True
    return False


def add_permission(settings: dict, rule: str) -> bool:
    """
    Add a permission rule if it doesn't already exist or isn't covered.
    Returns True if the rule was added.
    """
    permissions = settings.setdefault("permissions", {})
    allow = permissions.setdefault("allow", [])
    deny = permissions.get("deny", [])

    # Don't add if already in deny list
    if rule in deny:
        log(f"SKIPPED (in deny list): {rule}")
        return False

    # Don't add if already exists
    if rule in allow:
        return False

    # Check if a more general rule already covers this
    # e.g., "Bash(git:*)" covers "Bash(git status:*)"
    for existing in allow:
        if existing.endswith("(*)"):
            tool_prefix = existing[:-3]
            if rule.startswith(tool_prefix + "("):
                return False  # Already covered by wildcard

    allow.append(rule)
    log(f"ADDED: {rule}")
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Main hook logic
# ──────────────────────────────────────────────────────────────────────────────

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)  # Non-blocking: don't interfere if input is malformed

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if not tool_name:
        sys.exit(0)

    # Load current settings
    settings = load_settings()

    changed = False

    # Ensure baseline permissions on first meaningful invocation
    marker_file = Path.home() / ".claude" / ".auto-adapt-mode-initialized"
    if not marker_file.exists():
        changed = ensure_baseline(settings)
        marker_file.touch()
        log("Baseline initialized")

    # Generalize the tool invocation into a permission rule
    rule = generalize_tool_permission(tool_name, tool_input)

    if rule:
        if add_permission(settings, rule):
            changed = True

    # Save if anything changed
    if changed:
        save_settings(settings)

    # Always succeed — never block tool execution
    sys.exit(0)


if __name__ == "__main__":
    main()
