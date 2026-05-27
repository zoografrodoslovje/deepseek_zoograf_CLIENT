"""Session persistence — save/load conversation histories."""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class SessionManager:
    """Manages saving and loading chat sessions."""

    def __init__(self, session_dir: str | None = None):
        if session_dir is None:
            session_dir = str(Path.home() / ".ds-cli" / "sessions")
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.current_session_id: Optional[str] = None
        self.current_title: str = "Untitled Session"

    def new_session(self, title: str = "Untitled Session") -> str:
        self.current_title = title
        self.current_session_id = datetime.now().strftime("session_%Y%m%d_%H%M%S")
        return self.current_session_id

    def save_session(self, messages: list[dict], metadata: dict | None = None) -> str:
        if not self.current_session_id:
            self.new_session()
        data = {
            "id": self.current_session_id,
            "title": self.current_title,
            "timestamp": datetime.now().isoformat(),
            "messages": messages,
            "metadata": metadata or {},
        }
        path = self.session_dir / f"{self.current_session_id}.json"
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return str(path)

    def load_session(self, session_id: str) -> dict | None:
        path = self.session_dir / f"{session_id}.json"
        if not path.exists():
            return None
        with open(path) as f:
            data = json.load(f)
        self.current_session_id = data["id"]
        self.current_title = data.get("title", "Loaded Session")
        return data

    def list_sessions(self) -> list[dict]:
        sessions = []
        for f in sorted(self.session_dir.glob("*.json"), reverse=True):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                sessions.append({
                    "id": data.get("id", f.stem),
                    "title": data.get("title", "Untitled"),
                    "timestamp": data.get("timestamp", ""),
                    "message_count": len(data.get("messages", [])),
                })
            except Exception:
                pass
        return sessions

    def delete_session(self, session_id: str) -> bool:
        path = self.session_dir / f"{session_id}.json"
        if path.exists():
            path.unlink()
            return True
        return False
