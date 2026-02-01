from src.cash_drawer_validation import validate_cash_drawer


# -----------------------------
# Core behavior tests
# -----------------------------

def test_balanced_drawer_returns_balanced():
    """
    expected_cash == 0 → BALANCED
    """
    result = validate_cash_drawer(
        cash_sales_amount=1000,
        non_cash_sales_amount=5000,
        cash_withdrawals_amount=600,
        cash_deposits_amount=400,
    )

    assert result["status"] == "BALANCED"
    assert result["expected_cash"] == 0
    assert result["difference_amount"] == 0


def test_overage_drawer_returns_overage():
    """
    expected_cash > 0 → OVERAGE
    """
    result = validate_cash_drawer(
        cash_sales_amount=1000,
        non_cash_sales_amount=3000,
        cash_withdrawals_amount=200,
        cash_deposits_amount=300,
    )

    assert result["status"] == "OVERAGE"
    assert result["expected_cash"] == 500
    assert result["difference_amount"] == 500


def test_shortage_drawer_returns_shortage():
    """
    expected_cash < 0 → SHORTAGE
    """
    result = validate_cash_drawer(
        cash_sales_amount=1000,
        non_cash_sales_amount=8000,
        cash_withdrawals_amount=900,
        cash_deposits_amount=300,
    )

    assert result["status"] == "SHORTAGE"
    assert result["expected_cash"] == -200
    assert result["difference_amount"] == -200


# -----------------------------
# Structural contract tests
# -----------------------------

def test_expected_cash_equals_difference_amount():
    """
    expected_cash must always equal difference_amount
    """
    result = validate_cash_drawer(
        cash_sales_amount=750,
        non_cash_sales_amount=1200,
        cash_withdrawals_amount=300,
        cash_deposits_amount=200,
    )

    assert result["expected_cash"] == result["difference_amount"]


def test_non_cash_sales_amount_does_not_affect_result():
    """
    non_cash_sales_amount must not influence the calculation
    """
    result_a = validate_cash_drawer(
        cash_sales_amount=500,
        non_cash_sales_amount=0,
        cash_withdrawals_amount=200,
        cash_deposits_amount=100,
    )

    result_b = validate_cash_drawer(
        cash_sales_amount=500,
        non_cash_sales_amount=999999,
        cash_withdrawals_amount=200,
        cash_deposits_amount=100,
    )

    assert result_a == result_b


def test_status_is_always_valid_value():
    """
    Status must be one of the allowed values
    """
    result = validate_cash_drawer(
        cash_sales_amount=100,
        non_cash_sales_amount=50,
        cash_withdrawals_amount=30,
        cash_deposits_amount=10,
    )

    assert result["status"] in ("BALANCED", "OVERAGE", "SHORTAGE")


# -----------------------------
# Boundary tests
# -----------------------------

def test_all_zero_inputs_return_balanced():
    """
    All zero inputs should yield BALANCED
    """
    result = validate_cash_drawer(
        cash_sales_amount=0,
        non_cash_sales_amount=0,
        cash_withdrawals_amount=0,
        cash_deposits_amount=0,
    )

    assert result["status"] == "BALANCED"
    assert result["expected_cash"] == 0
    assert result["difference_amount"] == 0


def test_deposits_exceed_cash_sales_returns_shortage():
    """
    Deposits greater than cash sales yield SHORTAGE
    """
    result = validate_cash_drawer(
        cash_sales_amount=300,
        non_cash_sales_amount=1000,
        cash_withdrawals_amount=0,
        cash_deposits_amount=500,
    )

    assert result["status"] == "SHORTAGE"
    assert result["expected_cash"] == -200
    assert result["difference_amount"] == -200
