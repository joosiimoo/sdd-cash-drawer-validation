# Cash Drawer Validation — Test Contract

This document defines the **test contract** derived from `SPEC.md` (v0.2).
If a test fails, the implementation is wrong — not the spec.

---

## 1. System Under Test (SUT)

The SUT is a **pure function** with the following logical signature:

validate_cash_drawer(

* cash_sales_amount: number
* non_cash_sales_amount: number
* cash_withdrawals_amount: number
* cash_deposits_amount: number
  ) -> dict

Expected output keys:

* status: string
* expected_cash: number
* difference_amount: number

This contract does NOT require:

* input validation
* rounding
* currency formatting
* persistence
* I/O
* logging

---

## 2. Core Behavior Tests

### 2.1 Balanced (expected_cash == 0)

Input:

* cash_sales_amount = 1000
* non_cash_sales_amount = 5000
* cash_withdrawals_amount = 600
* cash_deposits_amount = 400

Calculation:

* expected_cash = 1000 - 600 - 400 = 0

Expected:

* status = BALANCED
* expected_cash = 0
* difference_amount = 0

---

### 2.2 Overage (expected_cash > 0)

Input:

* cash_sales_amount = 1000
* non_cash_sales_amount = 3000
* cash_withdrawals_amount = 200
* cash_deposits_amount = 300

Calculation:

* expected_cash = 1000 - 200 - 300 = 500

Expected:

* status = OVERAGE
* expected_cash = 500
* difference_amount = 500

---

### 2.3 Shortage (expected_cash < 0)

Input:

* cash_sales_amount = 1000
* non_cash_sales_amount = 8000
* cash_withdrawals_amount = 900
* cash_deposits_amount = 300

Calculation:

* expected_cash = 1000 - 900 - 300 = -200

Expected:

* status = SHORTAGE
* expected_cash = -200
* difference_amount = -200

---

## 3. Structural Contract Tests

### 3.1 expected_cash equals difference_amount (always)

For any valid input:

* expected_cash must equal difference_amount

Example assertion:

* result["expected_cash"] == result["difference_amount"]

---

### 3.2 non_cash_sales_amount does not affect output

The result must be identical when only non_cash_sales_amount changes.

Inputs A:

* cash_sales_amount = 500
* non_cash_sales_amount = 0
* cash_withdrawals_amount = 200
* cash_deposits_amount = 100

Inputs B:

* cash_sales_amount = 500
* non_cash_sales_amount = 999999
* cash_withdrawals_amount = 200
* cash_deposits_amount = 100

Expected:

* output(A) == output(B)

---

### 3.3 Status must be one of the allowed values

Allowed statuses:

* BALANCED
* OVERAGE
* SHORTAGE

Expected:

* result["status"] is one of these exact values

---

## 4. Boundary Tests

### 4.1 All zeros yields BALANCED

Input:

* cash_sales_amount = 0
* non_cash_sales_amount = 0
* cash_withdrawals_amount = 0
* cash_deposits_amount = 0

Expected:

* status = BALANCED
* expected_cash = 0
* difference_amount = 0

---

### 4.2 Deposits exceed cash sales yields SHORTAGE

Input:

* cash_sales_amount = 300
* non_cash_sales_amount = 1000
* cash_withdrawals_amount = 0
* cash_deposits_amount = 500

Calculation:

* expected_cash = 300 - 0 - 500 = -200

Expected:

* status = SHORTAGE
* expected_cash = -200
* difference_amount = -200

---

## 5. Out of Scope (No Tests)

The following behaviors are explicitly excluded from this test contract:

* missing field handling
* type validation
* negative value validation
* rounding rules
* thresholds/tolerances
* persistence
* notifications
* integration with any upstream/downstream systems

---

## 6. Implementation Constraints (Derived)

An implementation that satisfies this contract must:

* be a pure function
* compute expected_cash exactly per spec formula
* set difference_amount equal to expected_cash
* classify status strictly by sign of expected_cash
* ignore non_cash_sales_amount for computation (but accept it as input)
