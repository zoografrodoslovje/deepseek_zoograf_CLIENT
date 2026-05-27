"""Shell command execution with safety confirmation."""
import asyncio
import shlex


async def _run_command(command: str) -> str:
    """Execute a shell command and return output."""
    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=".",
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
        except asyncio.TimeoutError:
            proc.kill()
            return "Error: Command timed out after 60 seconds"

        output = ""
        if stdout:
            output += stdout.decode("utf-8", errors="replace")
        if stderr:
            if output:
                output += "\\n"
            output += stderr.decode("utf-8", errors="replace")

        result = f"Exit code: {proc.returncode}\\n"
        if output:
            result += output
        return result
    except FileNotFoundError:
        return f"Error: Command not found: {command}"
    except Exception as e:
        return f"Error executing command: {e}"


# Simple sync wrapper for the tool registry
# The actual confirmation happens at the UI level
_command_pending_confirmation = None


def execute_command(command: str, description: str = "") -> str:
    """Execute a shell command. NOTE: confirmation is handled by the UI layer."""
    global _command_pending_confirmation
    _command_pending_confirmation = {
        "command": command,
        "description": description,
    }
    # This raises a signal to the UI layer - the UI will handle
    # confirmation and rerun if approved
    raise CommandRequiresConfirmation(command, description)


class CommandRequiresConfirmation(Exception):
    """Raised when a shell command needs user confirmation."""
    def __init__(self, command: str, description: str = ""):
        self.command = command
        self.description = description
        super().__init__(f"Command requires confirmation: {command}")


async def execute_command_approved(command: str) -> str:
    """Execute a command that has been confirmed by the user."""
    return await _run_command(command)
