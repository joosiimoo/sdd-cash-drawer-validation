# Cash Drawer Validation — Feature Spec v0.2

---

## 1. Purpose

This feature validates the **cash drawer balance** for a given business day,
store and POS (cash drawer) using **only recorded system movements**.

It is a **pure validation feature** whose sole responsibility is to compute
the expected remaining cash and classify the result.

This feature is:

* deterministic
* read-only
* side-effect free

---

## 2. Temporal & Entity Scope

The validation is executed for **exactly one scope**:

* business day
* store
* POS (cash drawer)

All input amounts are assumed to already be **filtered to this scope upstream**.

This feature:

* does **not** perform date filtering
* does **not** resolve store or POS relationships
* does **not** aggregate data

---

## 3. Conceptual Model

There is **no physical cash count input**.

The system does **not** know how much cash is physically present in the drawer.

Instead, it computes the **expected remaining cash** based purely on
recorded cash movements.

The result represents:

* the cash the system expects to still be in the drawer
* an operational difference that must be explained externally

This feature **does not attempt** to explain the cause of the difference.

---

## 4. Inputs

All inputs are **required**, **numeric**, and **validated upstream**.

Behavior for missing or invalid inputs is **out of scope**.

Fields:

* cash_sales_amount: Total sales paid in cash
* non_cash_sales_amount: Total sales paid via non-cash methods
* cash_withdrawals_amount: Cash withdrawn from the drawer
* cash_deposits_amount: Cash deposited from the drawer

---

## 5. Explicit Clarification — non_cash_sales_amount

non_cash_sales_amount **does not participate in the calculation**.

It exists to:

* make the sales mix explicit
* avoid hidden assumptions about missing channels
* preserve domain clarity

Implementations **must not**:

* remove this field
* include it in calculations
* infer behavior from it

---

## 6. Calculation Logic

### 6.1 Expected Cash Formula

expected_cash = cash_sales_amount - cash_withdrawals_amount - cash_deposits_amount

### 6.2 Difference Semantics

difference_amount = expected_cash

Interpretation:

* difference is measured relative to a **zero-close assumption**
* no comparison against physical cash is performed

---

## 7. Status Classification

Rules:

* if expected_cash == 0 → status = BALANCED
* if expected_cash > 0 → status = OVERAGE
* if expected_cash < 0 → status = SHORTAGE

### Status Semantics

Statuses are defined **from the system’s point of view**:

* BALANCED
  → No remaining expected cash

* OVERAGE
  → The system expects cash still remaining in the drawer

* SHORTAGE
  → More cash left the drawer than recorded

The system does **not** infer:

* fraud
* error type
* responsibility

---

## 8. Output

The feature returns the following JSON structure:

{
"status": "BALANCED | OVERAGE | SHORTAGE",
"expected_cash": number,
"difference_amount": number
}

Output guarantees:

* expected_cash and difference_amount are always equal
* exactly one status is returned
* same input always produces the same output
* no rounding or currency formatting is applied

---

## 9. Explicit Non-Goals (Out of Scope)

This feature does NOT:

* correct the cash drawer
* generate accounting entries
* notify users or systems
* persist historical data
* compare against physical cash counts
* infer root cause or responsibility
* apply tolerances or thresholds

---

## 10. Determinism & Side Effects

* purely functional
* no side effects
* no I/O
* does not mutate state
* safe to re-run at any time

---

## 11. Agent-Readiness Statement

This specification is intentionally:

* explicit
* closed
* non-heuristic

Agents implementing this feature must not:

* infer additional business rules
* add validations
* introduce side effects
* “improve” the logic

---

## 12. Spec Status

Version: v0.2
State: Closed for implementation
Next step: Test-driven implementation via Cursor
