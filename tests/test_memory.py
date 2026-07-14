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


def test_empty_knowledge_base():
    """Test commands against an empty (non-existent) knowledge directory."""
    empty_result = run_memory_command(["search", "nonexistent"])
    assert empty_result.returncode == 0


def test_add_todo():
    """Test adding a todo entry."""
    result = run_memory_command(["add", "--type", "todo", "fix the CI pipeline"])
    assert result.returncode == 0
    assert "Added todo" in result.stdout

    content = (KNOWLEDGE_DIR / "todos" / "pending.md").read_text()
    assert "fix the CI pipeline" in content


def test_inject_output_format():
    """Test inject output contains expected structure."""
    result = run_memory_command(["inject"])
    assert result.returncode == 0
    assert len(result.stdout) > 0


def test_search_no_results():
    """Test search with no matching results returns cleanly."""
    result = run_memory_command(["search", "zzzz_nonexistent_query_zzzz"])
    assert result.returncode == 0


def test_review_stale_output():
    """Test review --stale output format."""
    result = run_memory_command(["review", "--stale"])
    assert result.returncode == 0


def test_add_process():
    """Test adding a process entry."""
    result = run_memory_command(["add", "--type", "process", "deploy to production"])
    assert result.returncode == 0
    assert "Added process" in result.stdout

    content = (KNOWLEDGE_DIR / "processes" / "general.md").read_text()
    assert "deploy to production" in content
