# Adding a New Feature (SDD + Cursor)

This repository follows **Spec-Driven Development (SDD)** with a
**Cursor-first, agent-native workflow**.

The goal is that **any engineer** can add a new feature **without asking questions**,
by following this playbook.

---

## Core Principle

> **Specs come first. Code is the last step.**

If behavior is not written in the spec, it must not exist in code.

---

## Feature Lifecycle (Mandatory Order)

1. Write or refine the spec
2. Generate the test contract
3. Implement using Cursor
4. Verify with tests
5. Commit

Skipping steps breaks the method.

---

## Step 1 — Write the Spec (Human + Agent)

Create or update a spec file (e.g. `SPEC.md` or `SPEC_<feature>.md`).

The spec **must be**:

* explicit
* closed (no “to be defined later”)
* deterministic
* free of heuristics

The spec **must define**:

* purpose
* scope
* inputs
* calculation rules
* output
* non-goals

### Rule

No code and no tests are written in this step.

---

## Step 2 — Generate the Test Contract (Agent 2)

From the spec, derive a **test contract**.

The test contract must:

* cover all business rules
* include happy paths and boundary cases
* explicitly exclude out-of-scope behavior

Tests are **the executable contract**.

If something is unclear in tests:
→ the spec is not ready.

---

## Step 3 — Create the Test File

Create a test file under `tests/`, for example:

```
tests/test_<feature_name>.py
```

Rules:

* tests must be deterministic
* no mocks
* no IO
* no shared state
* no hidden helpers

Tests should read like business rules.

---

## Step 4 — Implement Using Cursor (Agent 3)

Create or update the implementation file under `src/`.

Example:

```
src/<feature_name>.py
```

### Cursor Prompt (recommended)

Use a strict prompt like:

> Implement the function(s) required by the tests.
>
> Constraints:
>
> * Follow the spec strictly
> * Satisfy all tests
> * Do not add validation, logging, or side effects
> * Do not refactor tests
> * Do not introduce extra behavior

Cursor should only implement **what tests demand**.

---

## Step 5 — Verify

Run:

```bash
pytest -v
```

All tests must pass.

If a test fails:

* fix the implementation
* or refine the spec and tests (never patch behavior silently)

---

## Step 6 — Commit with Intent

Recommended commit message format:

```
feat: implement <feature_name> per spec vX.Y
```

This makes the evolution of specs and behavior traceable.

---

## Anti-Patterns (Do NOT Do This)

❌ Start coding before the spec is closed
❌ Add behavior “because it makes sense”
❌ Fix failing tests by weakening assertions
❌ Add validation not defined in the spec
❌ Use Cursor without constraints

---

## Why This Works with AI

* Closed specs remove ambiguity
* Tests remove interpretation
* Cursor becomes an execution engine, not a decision-maker
* The system scales from small features to complex domains

---

## Final Rule

If you need to explain behavior in a meeting or chat:
→ it belongs in the spec
→ not in code
→ not in comments

---

**This file is the contract for collaboration.**
If everyone follows it, features are reproducible, reviewable, and AI-compatible.
