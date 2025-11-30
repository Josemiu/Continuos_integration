import pytest
from membership_system import MembershipManager

# Inicializar el Manager para todas las pruebas
@pytest.fixture
def manager():
    return MembershipManager()

# ----------------------------------------------------
# Pruebas de Cálculo de Costo Base 
# ----------------------------------------------------

def test_basic_membership_cost(manager):
    """Prueba el costo base del plan 'basic' sin extras ni descuentos."""
    # Plan Básico: $50, 1 miembro, confirmado
    expected_cost = 50
    assert manager.calculate_cost("basic", [], 1, True) == expected_cost

def test_premium_membership_cost_with_features(manager):
    """Prueba el costo de membresía 'premium' con características estándar."""
    # Plan Premium: $100 + training $35 + group $20 = $155
    expected_cost = 155
    assert manager.calculate_cost("premium", ["personal_training", "group_classes"], 1, True) == expected_cost

# ----------------------------------------------------
# Pruebas de Descuento Grupal 
# ----------------------------------------------------

def test_group_discount_applied(manager):
    """Prueba el descuento del 10% por 2 o más miembros."""
    # Plan Básico: $50 * 2 miembros = $100. Descuento 10% ($10) = $90
    expected_cost = 90
    assert manager.calculate_cost("basic", [], 2, True) == expected_cost

def test_group_discount_with_features(manager):
    """Prueba el descuento grupal aplicado a un costo mayor."""
    # Plan Premium ($100) + training ($35) = $135
    # * 3 miembros = $405
    # - Descuento 10% ($40.50) = $364.50 -> Redondea a $365
    expected_cost = 365
    assert manager.calculate_cost("premium", ["personal_training"], 3, True) == expected_cost

# ----------------------------------------------------
# Pruebas de Recargo Premium (Req. 6)
# ----------------------------------------------------

def test_premium_surcharge_applied(manager):
    """Prueba el recargo del 15% por característica premium (exclusive_facilities)."""
    # Plan Básico $50 + exclusive_facilities $40 = $90
    # Recargo 15% sobre $90 = $13.50. Total = $103.50 -> Redondea a $104
    expected_cost = 104
    assert manager.calculate_cost("basic", ["exclusive_facilities"], 1, True) == expected_cost

def test_surcharge_and_group_discount_combined(manager):
    """Prueba que el recargo se aplica primero y luego el descuento grupal."""
    # Plan Básico $50 + specialized_training $50 = $100 (por miembro)
    # * 2 miembros = $200
    # 1. Aplicar Recargo 15%: $200 * 1.15 = $230
    # 2. Aplicar Descuento Grupal 10%: $230 * 0.90 = $207
    expected_cost = 207
    assert manager.calculate_cost("basic", ["specialized_training"], 2, True) == expected_cost
    
# ----------------------------------------------------
# Pruebas de Descuentos por Oferta Especial 
# ----------------------------------------------------

def test_special_offer_20_applied(manager):
    """Prueba el descuento de $20 cuando el costo > $200."""
    # Plan Family ($120) + training ($35) + classes ($20) = $175
    # * 2 miembros = $350
    # - Descuento 10% (grupo): $35. Total: $315
    # - Descuento oferta ($315 > $200): $20. Total: $295
    expected_cost = 295
    assert manager.calculate_cost("family", ["personal_training", "group_classes"], 2, True) == expected_cost

def test_special_offer_50_applied(manager):
    """Prueba el descuento de $50 cuando el costo > $400."""
    # Plan Premium ($100) + training ($35) + classes ($20) + pool ($15) = $170
    # * 3 miembros = $510
    # - Descuento 10% (grupo): $51. Total: $459
    # - Descuento oferta ($459 > $400): $50. Total: $409
    expected_cost = 409
    assert manager.calculate_cost("premium", ["personal_training", "group_classes", "pool_access"], 3, True) == expected_cost

# ----------------------------------------------------
# Pruebas de Validación y Salida 
# ----------------------------------------------------

def test_return_minus_one_on_cancel(manager):
    """Prueba que devuelve -1 si el usuario cancela (confirmed=False)."""
    assert manager.calculate_cost("basic", [], 1, False) == -1

def test_return_minus_one_on_invalid_plan(manager):
    """Prueba que devuelve -1 si el plan no existe."""
    assert manager.calculate_cost("super_vip", [], 1, True) == -1

def test_return_minus_one_on_invalid_feature(manager):
    """Prueba que devuelve -1 si la característica no existe."""
    assert manager.calculate_cost("basic", ["time_machine"], 1, True) == -1

def test_return_minus_one_on_invalid_members(manager):
    """Prueba que devuelve -1 si el número de miembros es cero o negativo."""
    assert manager.calculate_cost("basic", [], 0, True) == -1
    assert manager.calculate_cost("basic", [], -5, True) == -1

# ----------------------------------------------------
# Pruebas de Integración Máxima
# ----------------------------------------------------

def test_max_integration_case(manager):
    """Prueba la combinación de grupo, premium y descuento por oferta."""
    # Plan Family ($120) + exclusive_facilities ($40) = $160
    # * 4 miembros = $640
    # 1. Aplicar Recargo 15% (Premium): $640 * 1.15 = $736
    # 2. Aplicar Descuento Grupal 10%: $736 * 0.90 = $662.40
    # 3. Aplicar Descuento Oferta ($662.40 > $400): $50. Total: $612.40
    # Redondea a $613
    expected_cost = 613
    assert manager.calculate_cost("family", ["exclusive_facilities"], 4, True) == expected_cost
