"""
System for managing gym memberships, calculating costs, and applying discounts.
"""

class MembershipManager:
    """
    Manages gym membership costs, additional features, and discounts.
    """
    # pylint: disable=too-few-public-methods

    PLAN_COSTS = {
        "basic": 50,
        "premium": 100,
        "family": 150
    }

    FEATURE_COSTS = {
        "personal_training": 35,
        "group_classes": 20,
        "specialized_training": 50,
        "exclusive_access": 40
    }

    # Premium features that trigger a surcharge
    PREMIUM_FEATURES = {"specialized_training", "exclusive_access"}
    SURCHARGE_RATE = 0.15

    GROUP_DISCOUNT_RATE = 0.10
    GROUP_MIN_MEMBERS = 2

    # Special offers thresholds and discounts
    SPECIAL_OFFERS = [
        (400, 50),  # If > 400, discount 50
        (200, 20)   # If > 200, discount 20
    ]

    def calculate_cost(self, plan: str, features: list, num_members: int) -> int:
        """
        Calculates the total membership cost based on requirements.

        Args:
            plan (str): The membership plan type.
            features (list): List of additional features.
            num_members (int): Number of members signing up.

        Returns:
            int: Total cost rounded to the nearest integer, or -1 if invalid.
        """
        # 1. Validation
        if num_members <= 0:
            return -1

        if plan not in self.PLAN_COSTS:
            return -1

        for feature in features:
            if feature not in self.FEATURE_COSTS:
                return -1

        # 2. Base Cost Calculation
        base_cost = self.PLAN_COSTS[plan]
        features_cost = sum(self.FEATURE_COSTS[f] for f in features)

        # Total per group before discounts/surcharges
        total_cost = (base_cost + features_cost) * num_members

        # 3. Premium Surcharge (Requisito 6)
        # "Apply an additional 15% surcharge to the total cost of memberships
        # including premium features."
        has_premium = any(f in self.PREMIUM_FEATURES for f in features)
        if has_premium:
            total_cost *= (1 + self.SURCHARGE_RATE)

        # 4. Group Discount (Requisito 4)
        # "If two or more members sign up... apply a 10% discount"
        if num_members >= self.GROUP_MIN_MEMBERS:
            total_cost *= (1 - self.GROUP_DISCOUNT_RATE)

        # 5. Special Offer Discounts (Requisito 5)
        # Checked against the total cost calculated so far
        discount_to_apply = 0
        for threshold, discount in self.SPECIAL_OFFERS:
            if total_cost > threshold:
                discount_to_apply = discount
                break # Apply only the highest applicable discount

        total_cost -= discount_to_apply

        # 6. Output (Requisito 9) - Positive integer
        final_cost = int(total_cost + 0.5)
        return final_cost if final_cost > 0 else 0
