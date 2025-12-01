"""
Unit tests for the MembershipManager class.
"""
# pylint: disable=redefined-outer-name

import pytest
from membership_system import MembershipManager

@pytest.fixture
def manager():
    """Fixture to provide a MembershipManager instance."""
    return MembershipManager()

def test_basic_plan_single_member(manager):
    """Test basic plan cost for a single member."""
    # Plan: Basic ($50)
    # Members: 1
    # Total: 50
    assert manager.calculate_cost("basic", [], 1) == 50

def test_family_plan_single_member(manager):
    """Test family plan cost for a single member."""
    # Plan: Family ($150)
    # Members: 1
    # Total: 150
    assert manager.calculate_cost("family", [], 1) == 150

def test_premium_surcharge(manager):
    """Test premium surcharge application."""
    # Plan: Premium ($100)
    # Feature: specialized_training ($50) -> Premium feature
    # Members: 1
    # Base: 100 + 50 = 150
    # Surcharge: 150 * 1.15 = 172.5
    # Round: 173
    assert manager.calculate_cost("premium", ["specialized_training"], 1) == 173

def test_group_discount_basic(manager):
    """Test group discount for basic plan."""
    # Plan: Basic ($50)
    # Members: 2 (Group discount 10% applies)
    # Base: 50 * 2 = 100
    # Discount: 100 * 0.90 = 90
    # Special offer: < 200, none
    assert manager.calculate_cost("basic", [], 2) == 90

def test_special_offer_20_off(manager):
    """Test special offer discount ($20 off)."""
    # Plan: Premium ($100)
    # Members: 3 (Group discount 10%)
    # Base: 100 * 3 = 300
    # Group Discount: 300 * 0.90 = 270
    # Total > 200 -> -$20
    # Final: 270 - 20 = 250
    assert manager.calculate_cost("premium", [], 3) == 250

def test_special_offer_50_off(manager):
    """Test special offer discount ($50 off)."""
    # Plan: Family ($150)
    # Members: 3 (Group discount 10%)
    # Base: 150 * 3 = 450
    # Group Discount: 450 * 0.90 = 405
    # Total > 400 -> -$50
    # Final: 405 - 50 = 355
    assert manager.calculate_cost("family", [], 3) == 355

def test_combined_surcharge_group_special(manager):
    """Test combination of surcharge, group discount, and special offer."""
    # Plan: Premium ($100)
    # Feature: specialized_training ($50) -> Surcharge
    # Members: 2
    # Base per member: 150
    # Total Base: 300
    # Surcharge (15%): 300 * 1.15 = 345
    # Group Discount (10%): 345 * 0.90 = 310.5
    # Special Offer (>200): 310.5 - 20 = 290.5
    # Round: 291
    assert manager.calculate_cost("premium", ["specialized_training"], 2) == 291

def test_invalid_member_count(manager):
    """Test validation for invalid member counts."""
    assert manager.calculate_cost("basic", [], 0) == -1
    assert manager.calculate_cost("basic", [], -5) == -1

def test_invalid_plan(manager):
    """Test validation for invalid plan names."""
    assert manager.calculate_cost("super_gold", [], 1) == -1

def test_invalid_feature(manager):
    """Test validation for invalid features."""
    assert manager.calculate_cost("basic", ["sauna"], 1) == -1
