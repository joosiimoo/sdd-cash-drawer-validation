# SDD – Cash Drawer Validation (Agent-Native POC)

This repository demonstrates how to build **retail domain features** using
**Spec-Driven Development (SDD)** and **agent-native workflows**.

The goal of this project is **not the code**, but the **method**:
- clear and closed specs
- tests as executable contracts
- zero implicit decisions
- compatibility with AI agents

---

## 🧠 Feature Overview

**Cash Drawer Validation** computes the expected remaining cash for a given:
- business day
- store
- POS (cash drawer)

It is a **pure validation feature**:
- deterministic
- read-only
- side-effect free

---

## ❌ What this feature does NOT do

- Does not correct the cash drawer
- Does not generate accounting entries
- Does not notify users or systems
- Does not persist historical data
- Does not compare against physical cash counts

---

## 📄 Key Documents

| File | Purpose |
|------|--------|
| `SPEC.md` | Canonical business specification |
| `TEST_CONTRACT.md` | Test contract derived from the spec |
| `ADD_NEW_FEATURE.md` | How to add new features using SDD + Cursor |

---

## ▶️ Running Tests

```bash
pip install -r requirements-dev.txt
pytest -v
