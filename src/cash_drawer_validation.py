def validate_cash_drawer(
    cash_sales_amount,
    non_cash_sales_amount,
    cash_withdrawals_amount,
    cash_deposits_amount,
):
    """
    Pure function that validates the expected cash remaining in a drawer.

    This implementation strictly follows SPEC.md v0.2:
    - no validation
    - no side effects
    - no use of non_cash_sales_amount in calculations
    """

    expected_cash = (
        cash_sales_amount
        - cash_withdrawals_amount
        - cash_deposits_amount
    )

    if expected_cash == 0:
        status = "BALANCED"
    elif expected_cash > 0:
        status = "OVERAGE"
    else:
        status = "SHORTAGE"

    return {
        "status": status,
        "expected_cash": expected_cash,
        "difference_amount": expected_cash,
    }


def reconcile_rendition(system_amounts, declared_amounts):
    """
    Pure function that reconciles system amounts with declared amounts.
    difference = declared_amount - system_amount per payment means.
    BALANCED iff all differences are 0; otherwise UNBALANCED.
    """
    differences = {
        "cash": declared_amounts["cash"] - system_amounts["cash"],
        "debit_card": declared_amounts["debit_card"] - system_amounts["debit_card"],
        "credit_card": declared_amounts["credit_card"] - system_amounts["credit_card"],
    }
    status = "BALANCED" if all(d == 0 for d in differences.values()) else "UNBALANCED"
    return {"status": status, "differences": differences}
