"""---
tags: [test, validation, frontmatter, unit_test]
provides: [frontmatter_validation_tests]
requires: [pytest, meta/scripts/frontmatter_utils.py]
---
Unit tests for frontmatter validation and auto-correction.

This module contains tests for the frontmatter validation and auto-correction
functionality implemented in meta/scripts/frontmatter_utils.py.
"""

import os
import sys
import pytest
import tempfile
from pathlib import Path
import yaml

# Add parent directory to path so we can import the module
sys.path.append(str(Path(__file__).parent.parent))
from meta.scripts.frontmatter_utils import (
    extract_frontmatter,
    validate_frontmatter,
    auto_correct_frontmatter,
    process_file
)

# Test fixtures

@pytest.fixture
def temp_config():
    """Create a test configuration."""
    return {
        "defaults": {
            "tags": ["draft"],
            "provides": [],
            "requires": []
        },
        "ignore": [
            "docs/🔒archive/**",
            "tests/fixtures/ignored/**"
        ]
    }

@pytest.fixture
def temp_md_file():
    """Create a temporary Markdown file with frontmatter."""
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        f.write(b"""---
tags: [test, validation]
provides: [test_data]
requires: [some_dependency]
---

# Test Document

This is a test document.
""")
        path = f.name
    
    yield Path(path)
    
    # Cleanup
    os.unlink(path)

@pytest.fixture
def temp_py_file():
    """Create a temporary Python file with frontmatter."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(b'''"""---
tags: [test, python]
provides: [test_function]
requires: [os, sys]
---
This is a test Python file.
"""

import os
import sys

def test_function():
    """This is a test function."""
    return True
''')
        path = f.name
    
    yield Path(path)
    
    # Cleanup
    os.unlink(path)

@pytest.fixture
def temp_invalid_md_file():
    """Create a temporary Markdown file with invalid frontmatter."""
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        f.write(b"""---
tags: test_tag
provides: test_data
requires: 123
---

# Test Document

This document has invalid frontmatter.
""")
        path = f.name
    
    yield Path(path)
    
    # Cleanup
    os.unlink(path)

@pytest.fixture
def temp_no_frontmatter_md_file():
    """Create a temporary Markdown file without frontmatter."""
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        f.write(b"""# Test Document

This document has no frontmatter.
""")
        path = f.name
    
    yield Path(path)
    
    # Cleanup
    os.unlink(path)

# Tests

def test_extract_frontmatter_markdown(temp_md_file):
    """Test extracting frontmatter from a Markdown file."""
    frontmatter = extract_frontmatter(temp_md_file)
    assert frontmatter is not None
    assert "tags" in frontmatter
    assert "provides" in frontmatter
    assert "requires" in frontmatter
    assert frontmatter["tags"] == ["test", "validation"]

def test_extract_frontmatter_python(temp_py_file):
    """Test extracting frontmatter from a Python file."""
    frontmatter = extract_frontmatter(temp_py_file)
    assert frontmatter is not None
    assert "tags" in frontmatter
    assert "provides" in frontmatter
    assert "requires" in frontmatter
    assert frontmatter["tags"] == ["test", "python"]

def test_extract_frontmatter_no_frontmatter(temp_no_frontmatter_md_file):
    """Test extracting frontmatter from a file without frontmatter."""
    frontmatter = extract_frontmatter(temp_no_frontmatter_md_file)
    assert frontmatter is None

def test_validate_frontmatter_valid():
    """Test validating valid frontmatter."""
    frontmatter = {
        "tags": ["test", "validation"],
        "provides": ["test_data"],
        "requires": ["some_dependency"]
    }
    config = {"defaults": {"tags": ["draft"], "provides": [], "requires": []}}
    errors = validate_frontmatter(frontmatter, config)
    assert len(errors) == 0

def test_validate_frontmatter_missing_fields():
    """Test validating frontmatter with missing fields."""
    frontmatter = {
        "tags": ["test"]
    }
    config = {"defaults": {"tags": ["draft"], "provides": [], "requires": []}}
    errors = validate_frontmatter(frontmatter, config)
    assert len(errors) == 2
    assert "Missing required field: provides" in errors
    assert "Missing required field: requires" in errors

def test_validate_frontmatter_invalid_types():
    """Test validating frontmatter with invalid types."""
    frontmatter = {
        "tags": "test",
        "provides": 123,
        "requires": {"key": "value"}
    }
    config = {"defaults": {"tags": ["draft"], "provides": [], "requires": []}}
    errors = validate_frontmatter(frontmatter, config)
    assert len(errors) == 3
    assert "Tags must be a list" in errors
    assert "provides must be a list" in errors
    assert "requires must be a list" in errors

def test_auto_correct_frontmatter():
    """Test auto-correcting frontmatter."""
    frontmatter = {
        "tags": "test",
        "provides": 123,
        "requires": {"key": "value"}
    }
    config = {"defaults": {"tags": ["draft"], "provides": [], "requires": []}}
    corrected, corrections = auto_correct_frontmatter(frontmatter, config)
    
    assert len(corrections) == 3
    assert "Converted tags from string to list" in corrections
    assert "Replaced invalid provides with empty list" in corrections
    assert "Replaced invalid requires with empty list" in corrections
    
    assert corrected["tags"] == ["test"]
    assert corrected["provides"] == []
    assert corrected["requires"] == []

def test_process_file_valid(temp_md_file, temp_config):
    """Test processing a file with valid frontmatter."""
    success, messages = process_file(temp_md_file, temp_config)
    assert success
    assert len(messages) == 1
    assert "Frontmatter validation passed" in messages[0]

def test_process_file_invalid(temp_invalid_md_file, temp_config):
    """Test processing a file with invalid frontmatter."""
    success, messages = process_file(temp_invalid_md_file, temp_config, auto_correct=False)
    assert not success
    assert len(messages) >= 3
    assert any("Tags must be a list" in msg for msg in messages)
    assert any("provides must be a list" in msg for msg in messages)
    assert any("requires must be a list" in msg for msg in messages)

def test_process_file_auto_correct(temp_invalid_md_file, temp_config):
    """Test processing a file with auto-correction."""
    # Make a copy to avoid modifying the original
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        f.write(temp_invalid_md_file.read_bytes())
        test_file = Path(f.name)
    
    try:
        success, messages = process_file(test_file, temp_config, auto_correct=True, dry_run=False)
        assert not success  # Still reports errors
        assert any("Auto-correction: Converted tags from string to list" in msg for msg in messages)
        
        # Verify the file was updated
        updated_frontmatter = extract_frontmatter(test_file)
        assert updated_frontmatter is not None
        assert isinstance(updated_frontmatter["tags"], list)
        assert updated_frontmatter["tags"] == ["test_tag"]
        assert isinstance(updated_frontmatter["provides"], list)
        assert updated_frontmatter["provides"] == ["test_data"]
        assert isinstance(updated_frontmatter["requires"], list)
        assert updated_frontmatter["requires"] == []
    finally:
        os.unlink(test_file)

def test_process_file_no_frontmatter_add(temp_no_frontmatter_md_file, temp_config):
    """Test processing a file without frontmatter and adding it."""
    # Make a copy to avoid modifying the original
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        f.write(temp_no_frontmatter_md_file.read_bytes())
        test_file = Path(f.name)
    
    try:
        success, messages = process_file(test_file, temp_config, auto_correct=True, dry_run=False)
        assert not success  # Reports no frontmatter
        assert any("No frontmatter found" in msg for msg in messages)
        assert any("Added default frontmatter" in msg for msg in messages)
        
        # Verify frontmatter was added
        updated_frontmatter = extract_frontmatter(test_file)
        assert updated_frontmatter is not None
        assert "tags" in updated_frontmatter
        assert updated_frontmatter["tags"] == ["draft"]
    finally:
        os.unlink(test_file) 