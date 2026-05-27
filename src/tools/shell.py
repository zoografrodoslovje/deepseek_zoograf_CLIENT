"""Shell Command Tools - Execute terminal commands"""

import asyncio
from typing import Optional


async def execute_command(command: str, timeout: int = 30) -> str:
    """Execute a shell command and return output.

    WARNING: This tool requires explicit user confirmation before execution
    for security purposes. Commands are run with restricted permissions.

    Args:
        command: Shell command to execute
        timeout: Maximum execution time in seconds (default: 30)

    Returns:
        Command output or error message
    """
    # Security check: deny dangerous commands
    dangerous_patterns = [
        "rm -rf",
        "dd if=/dev/",
        ":(){:|:&};:",  # Fork bomb
        "mkfs",
        "shutdown",
        "reboot",
        "poweroff",
        ":() { :|:& };:",
        "*:*",  # Path manipulation
    ]

    command_lower = command.lower().strip()

    for pattern in dangerous_patterns:
        if pattern in command_lower:
            return f"Dangerous command blocked: '{command}'"

    # Also block write operations to system directories
    if any(x in command for x in ["/etc/", "/bin/", "/sbin/"]):
        return f"System directory access denied: '{command}'"

    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=timeout
        )

        output = ""

        if stdout:
            output += stdout.decode("utf-8", errors="replace")

        if stderr:
            output += f"[STDERR] {stderr.decode('utf-8', errors='replace')}"

        exit_code = process.returncode

        result = f"Command executed:\n\n```\n{command}\n```\n\nExit code: {exit_code}"

        if output.strip():
            result += f"\n\nOutput:\n```\n{output.strip()}\n```"
        else:
            result += "\n\n[No output]"

        return result

    except asyncio.TimeoutError:
        return f"Command timed out after {timeout} seconds: '{command}'"
    except Exception as e:
        return f"Error executing command: {str(e)}"


def require_confirmation(command: str) -> bool:
    """Check if a command requires user confirmation.

    Args:
        command: Shell command to check

    Returns:
        True if confirmation is required
    """
    # Always require confirmation for write/delete operations
    write_commands = ["rm ", "rmdir ", "mv ", "cp ", "touch ", "echo >", "> "]

    return any(cmd in command.lower() for cmd in write_commands)


__all__ = ["execute_command", "require_confirmation"]
