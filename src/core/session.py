"""Session Management - Save/Load Chat Histories"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class SessionManager:
    """Manages saving and loading chat sessions."""

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize session manager.

        Args:
            storage_dir: Directory to store session files (default: ./sessions/)
        """
        self.storage_dir = storage_dir or Path("./sessions")
        self.current_session_id: str | None = None

        # Create storage directory if it doesn't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def create_session(self, name: Optional[str] = None) -> str:
        """Create a new session.

        Args:
            name: Optional session name

        Returns:
            Unique session ID
        """
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_name = name or f"Session {session_id}"

        metadata = {
            "id": session_id,
            "name": session_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        # Start with empty messages
        session_data = {"metadata": metadata, "messages": [], "tool_calls": []}
        await self._save_session(session_id, session_data)

        self.current_session_id = session_id
        return session_id

    async def load_session(self, session_id: str) -> Optional[dict[str, Any]]:
        """Load a session by ID.

        Args:
            session_id: Session ID to load

        Returns:
            Session data dictionary or None if not found
        """
        session_file = self.storage_dir / f"{session_id}.json"

        if not session_file.exists():
            return None

        content = session_file.read_text()
        return json.loads(content)

    async def save_session(
        self, session_id: str, messages: list[dict], tool_calls: list[dict] = []
    ) -> bool:
        """Save current session data.

        Args:
            session_id: Session ID to save
            messages: Current message history
            tool_calls: List of tool call records

        Returns:
            True if saved successfully
        """
        try:
            # Load existing session to preserve metadata
            existing = await self.load_session(session_id)
            metadata = existing.get("metadata", {}) if existing else {}

            session_data = {
                "metadata": metadata,
                "messages": messages,
                "tool_calls": tool_calls,
                "updated_at": datetime.now().isoformat(),
            }

            session_file = self.storage_dir / f"{session_id}.json"
            session_file.write_text(json.dumps(session_data, indent=2))
            return True

        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session.

        Args:
            session_id: Session ID to delete

        Returns:
            True if deleted successfully
        """
        session_file = self.storage_dir / f"{session_id}.json"

        if not session_file.exists():
            return False

        try:
            session_file.unlink()
            if self.current_session_id == session_id:
                self.current_session_id = None
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    async def list_sessions(self) -> list[dict[str, Any]]:
        """List all available sessions.

        Returns:
            List of session metadata dictionaries
        """
        sessions = []

        for session_file in self.storage_dir.glob("*.json"):
            session_id = session_file.stem
            session_data = await self.load_session(session_id)

            if session_data:
                metadata = session_data.get("metadata", {})
                messages_count = len(session_data.get("messages", []))

                sessions.append(
                    {
                        "id": session_id,
                        "name": metadata.get("name", f"Session {session_id}"),
                        "created_at": metadata.get("created_at"),
                        "updated_at": metadata.get("updated_at"),
                        "message_count": messages_count,
                    }
                )

        # Sort by updated_at descending
        sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return sessions

    async def branch_session(self, source_id: str, new_name: str | None = None) -> str:
        """Create a branch from an existing session.

        Args:
            source_id: Source session ID to branch from
            new_name: Optional name for the new branch

        Returns:
            New branch session ID
        """
        source_session = await self.load_session(source_id)

        if not source_session:
            raise ValueError(f"Source session {source_id} not found")

        # Create new session with copied messages
        new_id = await self.create_session(new_name)
        new_session = await self.load_session(new_id)

        if new_session:
            # Copy messages and tool calls
            new_session["messages"] = source_session.get("messages", [])
            new_session["tool_calls"] = source_session.get("tool_calls", [])
            new_session["updated_at"] = datetime.now().isoformat()
            await self.save_session(new_id, new_session["messages"], new_session["tool_calls"])

        return new_id
