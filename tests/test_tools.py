"""Unit Tests for Tools Module"""

import pytest
from pathlib import Path
import tempfile
import shutil


class TestFileSystemTools:
    """Tests for file system tools."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_path = tempfile.mkdtemp()
        yield Path(temp_path)
        shutil.rmtree(temp_path, ignore_errors=True)

    def test_read_file_exists(self, temp_dir):
        """Test reading an existing file."""
        from src.tools.filesystem import read_file

        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello World")

        result = read_file(str(test_file.relative_to(temp_dir)))
        assert "Successfully read" in result
        assert "Hello World" in result

    def test_read_file_not_found(self, temp_dir):
        """Test reading a non-existent file."""
        from src.tools.filesystem import read_file

        result = read_file("nonexistent.txt")
        assert "not found" in result.lower()

    def test_list_dir(self, temp_dir):
        """Test listing directory contents."""
        from src.tools.filesystem import list_dir

        # Create some test files
        (temp_dir / "file1.txt").touch()
        (temp_dir / "file2.py").touch()

        result = list_dir(str(temp_dir))
        assert "file1.txt" in result
        assert "file2.py" in result

    def test_write_file(self, temp_dir):
        """Test writing to a file."""
        from src.tools.filesystem import write_file

        relative_path = "new_test.txt"
        result = write_file(relative_path, "New content", str(temp_dir))

        assert "Successfully wrote" in result
        assert (temp_dir / relative_path).exists()


class TestShellTools:
    """Tests for shell command tools."""

    def test_dangerous_command_blocked(self):
        """Test that dangerous commands are blocked."""
        from src.tools.shell import execute_command

        result = asyncio.run(execute_command("rm -rf /"))
        assert "Dangerous command blocked" in result or "Error" in result


class TestRegistry:
    """Tests for tool registry."""

    def test_get_all_tools(self):
        """Test getting all registered tools."""
        from src.tools.registry import get_all_tools

        tools = get_all_tools()
        assert len(tools) >= 3  # At least read_file, list_dir, etc.

        # Each tool should have required structure
        for tool in tools:
            assert "type" in tool
            assert "function" in tool["function"]
