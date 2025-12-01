"""
Main entry point for the Gym Membership System CLI.
"""
import sys
from membership_system import MembershipManager

def main():
    """
    Main function to run the CLI application.
    Prompts user for inputs and displays results.
    """
    manager = MembershipManager()
    print("=== Gym Membership System ===")

    # 1. Membership Selection
    print("\nAvailable Plans:")
    for plan, cost in manager.PLAN_COSTS.items():
        print(f"- {plan}: ${cost}")
    
    selected_plan = input("\nSelect a membership plan: ").strip().lower()
    if selected_plan not in manager.PLAN_COSTS:
        print("Error: Invalid plan selected.")
        return -1

    # 2. Additional Features
    print("\nAvailable Features:")
    for feature, cost in manager.FEATURE_COSTS.items():
        print(f"- {feature}: ${cost}")
    
    print("\nEnter features separated by comma (or press Enter for none):")
    features_input = input("> ").strip().lower()
    selected_features = [f.strip() for f in features_input.split(",") if f.strip()]
    
    # Validate features
    for f in selected_features:
        if f not in manager.FEATURE_COSTS:
            print(f"Error: Feature '{f}' is not available.")
            return -1

    # 3. Member Count
    try:
        num_members = int(input("\nEnter number of members: "))
        if num_members <= 0:
            raise ValueError
    except ValueError:
        print("Error: Invalid number of members.")
        return -1

    # 4. User Confirmation
    print("\n--- Confirmation ---")
    print(f"Plan: {selected_plan}")
    print(f"Features: {', '.join(selected_features) if selected_features else 'None'}")
    print(f"Members: {num_members}")
    
    confirm = input("\nConfirm these details? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled by user.")
        return -1

    # 5. Final Calculation & Output
    total_cost = manager.calculate_cost(selected_plan, selected_features, num_members)
    
    if total_cost != -1:
        print(f"\nTotal Membership Cost: ${total_cost}")
        return total_cost

    print("Error calculating cost.")
    return -1

if __name__ == "__main__":
    sys.exit(main())
