import subprocess
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def run_memory_command(args: list[str]) -> subprocess.CompletedProcess:
    """Run the assistant-memory CLI tool with the given arguments."""
    return subprocess.run(
        ["bin/assistant-memory"] + args,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

def test_add_learning():
    """Test adding a learning entry."""
    # Ensure the learnings directory and file exist
    learnings_dir = KNOWLEDGE_DIR / "learnings"
    learnings_dir.mkdir(exist_ok=True)
    (learnings_dir / "general.md").touch()

    # Add a learning
    result = run_memory_command(["add", "--type", "learning", "test learning"])
    assert result.returncode == 0
    assert "Added learning" in result.stdout

    # Verify the learning was added
    content = (learnings_dir / "general.md").read_text()
    assert "test learning" in content

def test_search():
    """Test searching for an entry."""
    result = run_memory_command(["search", "test"])
    assert result.returncode == 0
    assert "test learning" in result.stdout

def test_review_stale():
    """Test reviewing stale entries."""
    result = run_memory_command(["review", "--stale"])
    assert result.returncode == 0

def test_inject():
    """Test injecting the knowledge base."""
    result = run_memory_command(["inject"])
    assert result.returncode == 0

def test_add_duplicate():
    """Test adding a duplicate entry."""
    run_memory_command(["add", "--type", "learning", "duplicate entry"])
    result = run_memory_command(["add", "--type", "learning", "duplicate entry"])
    assert result.returncode == 0
    content = (KNOWLEDGE_DIR / "learnings" / "general.md").read_text()
    assert content.count("duplicate entry") == 2

def test_add_with_special_characters():
    """Test adding an entry with special characters."""
    special_string = "!@#$%^&*()_+-=[]{};':\",./<>?`~"
    result = run_memory_command(["add", "--type", "learning", special_string])
    assert result.returncode == 0
    content = (KNOWLEDGE_DIR / "learnings" / "general.md").read_text()
    assert special_string in content
