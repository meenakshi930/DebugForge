# DebugForge

**Autonomous Debugging and Code Repair Agent**

DebugForge is an AI-powered debugging agent that automatically analyzes failing Python tests, identifies the likely source of the bug, generates a minimal code patch, applies the patch in an isolated workspace, and verifies the repair by running the tests again.

It is designed as a developer tool for **autonomous code debugging and repair**.

---

## 🚀 How It Works

DebugForge follows an iterative debugging loop:

```text
Repository
    │
    ▼
Run Tests
    │
    ▼
Detect Failure
    │
    ▼
Parse Test Failure
    │
    ▼
Localize Source Code
    │
    ▼
Extract Relevant Function
    │
    ▼
Send Context to NVIDIA Nemotron
    │
    ▼
Generate Structured Patch
    │
    ▼
Validate Patch
    │
    ▼
Apply Patch
    │
    ▼
Run Tests Again
    │
    ├── PASS ──► VERIFIED
    │
    └── FAIL ──► Retry Repair
```

The agent can make multiple repair attempts when the first generated patch does not pass verification.

---

## ✨ Features

- Automatic execution of Python test suites
- Failure detection and parsing
- Test failure localization
- Source-code localization
- Relevant function extraction using Python AST
- AI-powered root-cause analysis
- Structured repair generation
- Exact old-code/new-code patching
- Patch validation before modification
- Isolated debugging workspace
- Automatic post-repair verification
- Retry loop for failed repairs
- Unified diff generation
- Attempt history tracking
- Command-line interface
- NVIDIA Nemotron integration through Nebius Token Factory

---

## 🧠 Why DebugForge?

Traditional debugging usually requires a developer to manually:

1. Run the tests
2. Read the error
3. Find the failing code
4. Understand the bug
5. Modify the code
6. Run the tests again
7. Repeat if the fix fails

DebugForge automates this loop.

Instead of asking an AI model to blindly rewrite an entire project, DebugForge provides the model with **evidence from the actual test execution** and asks it to produce a small, structured repair.

The generated patch is then verified by executing the tests again.

This makes the system **test-driven rather than generation-driven**.

---

## 🏗️ Architecture

```text
                 ┌──────────────────┐
                 │    Buggy Repo    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Test Runner    │
                 │      pytest      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Failure Parser  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Source Localizer │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Source Context   │
                 │   Extraction     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ NVIDIA Nemotron  │
                 │    via Nebius    │
                 └────────┬─────────┘
                          │
                          ▼
                