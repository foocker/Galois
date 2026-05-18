# Thin Workspace Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop copying the vendored generator for each project and create a thin workspace with static symlinks plus writable runtime directories.

**Architecture:** `references/Lumen` remains the immutable asset source. Project workspaces contain symlinks for static generator files/directories and real directories for mutable runtime state. Run-specific snapshots and logs stay under each run directory.

**Tech Stack:** Python, FastAPI, pytest, pathlib.

---

### Task 1: Lock Thin Workspace Behavior

**Files:**
- Modify: `tests/test_agent_runtime_api.py`

- [ ] **Step 1: Write the failing test**
  Add a test that creates a project, inspects the generated workspace, and asserts static entries are symlinks while writable directories are real directories.

- [ ] **Step 2: Run test to verify it fails**
  Run: `uv run pytest tests/test_agent_runtime_api.py::test_project_workspace_uses_static_symlinks_and_writable_dirs -q`
  Expected: FAIL because current implementation copies static assets.

### Task 2: Implement Thin Workspace Setup

**Files:**
- Modify: `src/agent_runtime/service.py`
- Modify: `README.md`
- Modify: `docs/AGENT_RUNTIME_API.md`

- [ ] **Step 3: Replace copy setup with thin workspace setup**
  Add constants for static entries and writable directories. Create missing symlinks from `references/Lumen/agents/generation` and create writable directories as real directories.

- [ ] **Step 4: Verify tests**
  Run targeted test, then full test suite and basic CLI checks.
