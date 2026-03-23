"""Verify no references to life-os, private data, or personal contacts remain."""
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN_PATTERNS = [
    r"life-os",
    r"\.claude/skills",
    r"\.claude\\skills",
    r"comms-state",
    r"comms-violations",
    r"financial-context",
    r"valuation-model",
    r"entity-map",
    r"operational-intelligence",
    r"market-benchmarks",
    r"sgomberg@ya\.ru",
    r"sgomberg@yandex\.ru",
    r"\+7\s?\d{3}\s?\d{3}",
    r"Telegram\s*(ID|id)\s*:\s*\d{6,}",
    r"sgomberg@",
    r"edgomberg@",
    r"tagiltseva-tv@",
    r"pramzelevsemyon@",
]

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", "data", "docs"}
SKIP_FILES = {".gitignore", "test_no_lifeos_refs.py", "CLAUDE.md"}


def _scan_files():
    """Yield (filepath, content) for all text files in repo."""
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if fname in SKIP_FILES:
                continue
            if not fname.endswith(
                (".py", ".sh", ".json", ".md", ".service", ".timer", ".txt", ".yml", ".yaml")
            ):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath) as f:
                    yield fpath, f.read()
            except (UnicodeDecodeError, PermissionError):
                continue


def test_no_lifeos_references():
    violations = []
    for fpath, content in _scan_files():
        rel = os.path.relpath(fpath, REPO_ROOT)
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, content):
                violations.append(f"{rel}: matches '{pattern}'")
    assert not violations, "Found forbidden references:\n" + "\n".join(violations)


def test_no_syspath_hacks():
    """No sys.path.insert referencing parent dirs more than one level up."""
    violations = []
    for fpath, content in _scan_files():
        if not fpath.endswith(".py"):
            continue
        rel = os.path.relpath(fpath, REPO_ROOT)
        for line_no, line in enumerate(content.splitlines(), 1):
            if "sys.path.insert" in line and line.count("'..'") > 1:
                violations.append(f"{rel}:{line_no}: {line.strip()}")
    assert not violations, "Found sys.path hacks:\n" + "\n".join(violations)
