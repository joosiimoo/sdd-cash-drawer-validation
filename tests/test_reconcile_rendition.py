"""
Test contract for reconcile_rendition (Reconcile Rendition).
Derived from TEST_CONTRACT_RECONCILE_RENDITION.md.
"""
from src.cash_drawer_validation import reconcile_rendition


# -----------------------------
# 6.1 Rendición completamente cuadrada
# -----------------------------


def test_rendition_completely_balanced():
    """BALANCED when system and declared match exactly; all differences 0."""
    system = {"cash": 100, "debit_card": 200, "credit_card": 300}
    declared = {"cash": 100, "debit_card": 200, "credit_card": 300}
    result = reconcile_rendition(system, declared)
    assert result["status"] == "BALANCED"
    assert result["differences"]["cash"] == 0
    assert result["differences"]["debit_card"] == 0
    assert result["differences"]["credit_card"] == 0


# -----------------------------
# 6.2 Sobrante en efectivo
# -----------------------------


def test_surplus_in_cash():
    """UNBALANCED when declared cash > system cash; cash difference +20."""
    system = {"cash": 100, "debit_card": 200, "credit_card": 300}
    declared = {"cash": 120, "debit_card": 200, "credit_card": 300}
    result = reconcile_rendition(system, declared)
    assert result["status"] == "UNBALANCED"
    assert result["differences"]["cash"] == 20
    assert result["differences"]["debit_card"] == 0
    assert result["differences"]["credit_card"] == 0


# -----------------------------
# 6.3 Faltante en tarjeta débito
# -----------------------------


def test_shortage_in_debit_card():
    """debit_card difference = declared - system = -20."""
    system = {"cash": 100, "debit_card": 200, "credit_card": 300}
    declared = {"cash": 100, "debit_card": 180, "credit_card": 300}
    result = reconcile_rendition(system, declared)
    assert result["differences"]["debit_card"] == -20
    assert result["differences"]["cash"] == 0
    assert result["differences"]["credit_card"] == 0


# -----------------------------
# 6.4 Diferencias en múltiples medios
# -----------------------------


def test_differences_in_multiple_means():
    """cash -10, debit_card +20, credit_card 0."""
    system = {"cash": 100, "debit_card": 200, "credit_card": 300}
    declared = {"cash": 90, "debit_card": 220, "credit_card": 300}
    result = reconcile_rendition(system, declared)
    assert result["differences"]["cash"] == -10
    assert result["differences"]["debit_card"] == 20
    assert result["differences"]["credit_card"] == 0


# -----------------------------
# 6.5 Todas las diferencias negativas
# -----------------------------


def test_all_differences_negative():
    """UNBALANCED; all differences < 0."""
    system = {"cash": 100, "debit_card": 200, "credit_card": 300}
    declared = {"cash": 80, "debit_card": 150, "credit_card": 250}
    result = reconcile_rendition(system, declared)
    assert result["status"] == "UNBALANCED"
    assert result["differences"]["cash"] == -20
    assert result["differences"]["debit_card"] == -50
    assert result["differences"]["credit_card"] == -50
