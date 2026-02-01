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
