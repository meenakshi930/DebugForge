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
                 │   Buggy Repo      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Test Runner     │
                 │     pytest       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Failure Parser   │
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
                 │   via Nebius     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Repair Parser    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Patch Validator  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Patch Applier    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Test Verifier    │
                 └────────┬─────────┘
                          │
                 ┌────────┴─────────┐
                 ▼                  ▼
              VERIFIED            FAILED
                                    │
                                    ▼
                              Retry Repair
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| pytest | Test execution and verification |
| NVIDIA Nemotron | AI reasoning and repair generation |
| Nebius Token Factory | Model API infrastructure |
| OpenAI Python SDK | API communication |
| Python AST | Function-level source extraction |
| subprocess | Test execution |
| dataclasses | Internal state and attempt tracking |
| difflib | Patch/diff generation |
| argparse | CLI |
| Git/GitHub | Version control |

---

## 🤖 NVIDIA + Nebius Integration

DebugForge uses **NVIDIA Nemotron** through **Nebius Token Factory**.

The model is used to analyze test failures and generate structured repair instructions.

Current model:

```text
nvidia/Nemotron-3_5-Lightning
```

The model receives information such as:

- Test status
- Failing test
- Error information
- Expected result
- Actual result
- Relevant source function
- Previous repair attempt when retrying

It must return a structured response:

```text
DIAGNOSIS:
<root cause>

FILE:
<file to modify>

OLD_CODE:
<existing code>

NEW_CODE:
<replacement code>
```

DebugForge then validates the proposed patch before applying it.

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
NEBIUS_API_KEY=your_api_key_here
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1/
NEBIUS_MODEL=nvidia/Nemotron-3_5-Lightning
```

Never commit your real API key.

A template is provided in:

```text
.env.example
```

---

## 📦 Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd DebugForge
```

Create a virtual environment:

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your `.env` file with your Nebius API key.

---

## 🧪 Run the Tests

The default test suite does not make external API calls:

```bash
pytest -m "not integration" -v
```

Integration tests that communicate with the real model are marked separately:

```text
@pytest.mark.integration
```

This prevents accidental API usage during normal development.

---

## ▶️ Run DebugForge

DebugForge provides a command-line interface.

General syntax:

```bash
python -m debugforge --repo <repository> --test "<test command>"
```

For example:

```bash
python -m debugforge --repo ./examples/buggy_project --test "pytest"
```

---

## 🐛 Example

The repository contains a deliberately buggy project:

```text
examples/
└── buggy_project/
    ├── app.py
    └── test_app.py
```

The original code contains:

```python
def add(a, b):
    return a - b
```

The test expects:

```python
assert add(2, 3) == 5
```

Running:

```bash
python -m debugforge --repo ./examples/buggy_project --test "pytest"
```

produces a debugging flow similar to:

```text
DebugForge
----------

Repository: ./examples/buggy_project
Test command: pytest

Running debugging agent...

Status: VERIFIED

Failure Analysis:
  Test file: test_app.py
  Test name: test_add
  Error: AssertionError
  Source file: app.py
  Source function: add

Repair:
  File: app.py
  Diagnosis: The `add` function performs subtraction instead of addition.

Verification: PASSED

Patch:
--- app.py (before)
+++ app.py (after)
@@ -1 +1 @@
-return a - b
+return a + b

✓ DebugForge successfully repaired the bug.
```

---

## 🔄 Autonomous Repair Loop

DebugForge does not assume that the first AI-generated repair will always be correct.

If a repair fails verification, DebugForge:

1. Records the previous attempt.
2. Runs the tests again.
3. Parses the new failure.
4. Re-localizes the source.
5. Provides the previous attempt to the model.
6. Requests a better repair.
7. Applies the new patch.
8. Verifies the result again.

The current maximum number of repair attempts is:

```text
3
```

This prevents the agent from entering an unlimited repair loop.

---

## 🛡️ Patch Safety

DebugForge does not blindly replace arbitrary code.

Before applying a patch, it checks that:

- `OLD_CODE` is not empty.
- `NEW_CODE` is not empty.
- `OLD_CODE` exists in the source.
- `OLD_CODE` occurs exactly once.
- `OLD_CODE` and `NEW_CODE` are different.

This reduces the chance of accidentally modifying the wrong section of code.

---

## 📁 Project Structure

```text
DebugForge/
│
├── debugforge/
│   ├── __init__.py
│   ├── __main__.py
│   ├── agent.py
│   ├── ai_agent.py
│   ├── attempt.py
│   ├── diagnosis.py
│   ├── diff_generator.py
│   ├── failure.py
│   ├── job.py
│   ├── localizer.py
│   ├── orchestrator.py
│   ├── patch_response.py
│   ├── patch_validator.py
│   ├── patcher.py
│   ├── pytest_parser.py
│   ├── repair_loop.py
│   ├── repair_parser.py
│   ├── retry_prompt.py
│   ├── runner.py
│   ├── source_context.py
│   ├── source_localizer.py
│   ├── verifier.py
│   └── workspace.py
│
├── tests/
│   ├── test_ai_agent.py
│   ├── test_patch_validator.py
│   ├── test_real_ai_agent.py
│   ├── test_real_repair.py
│   └── test_orchestrator.py
│
├── examples/
│   └── buggy_project/
│       ├── app.py
│       └── test_app.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 🧩 Design Principles

### Test-driven repair

The test suite provides the evidence used to determine whether a repair is successful.

### Minimal patches

The model is instructed to make the smallest safe change rather than rewriting an entire file.

### Isolated execution

DebugForge copies the target repository into a temporary workspace before modifying it.

The original repository is therefore protected from direct modification.

### Structured model output

Instead of accepting arbitrary natural-language responses, DebugForge requires the model to return:

```text
DIAGNOSIS
FILE
OLD_CODE
NEW_CODE
```

This makes the AI response easier to validate and process programmatically.

### Verification before success

A generated patch is not considered successful simply because the model produced it.

The repair is successful only when the tests pass.

---

## 📊 Current Capabilities

DebugForge currently supports:

- Python repositories
- pytest-based testing
- Function-level source localization
- AI-generated code repairs
- Patch validation
- Automatic verification
- Retry-based repair
- CLI execution
- NVIDIA Nemotron through Nebius Token Factory

---

## 🚧 Current Limitations

DebugForge is currently focused on Python and pytest workflows.

Some advanced debugging scenarios are not yet supported, including:

- Complex multi-file dependency analysis
- Large-scale architectural bugs
- Non-Python projects
- Non-pytest test frameworks
- Semantic patch validation beyond test execution
- Complex database or infrastructure failures
- Human approval workflows
- Full repository-wide code understanding

These are potential areas for future development.

---

## 🔮 Future Improvements

Potential future extensions include:

- Multi-file repair
- Better stack-trace analysis
- Repository-wide dependency graphs
- Static analysis integration
- Security-aware patch validation
- Human-in-the-loop approval
- Git-based patch commits
- Support for additional programming languages
- Support for additional testing frameworks
- Rich web interface for debugging sessions
- Persistent debugging history
- Better regression-test generation
- More sophisticated patch verification

---

## 🎯 Hackathon Track

DebugForge is built for the **Coding and Agentic Engineering** track.

The project focuses on an autonomous developer workflow where an AI agent can:

```text
Understand failure
      ↓
Reason about the bug
      ↓
Write a repair
      ↓
Run the code
      ↓
Test the repair
      ↓
Retry when necessary
```

The goal is to move beyond simple code generation toward an **agent that can execute and verify its own engineering work**.

---

## 👩‍💻 Author

Built as an AI/ML engineering project for the **Nebius × NVIDIA Global AI Hackathon 2026**.

---

## 📄 License

This project is released under the **MIT License**.
