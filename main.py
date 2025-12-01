"""
Main entry point for the Gym Membership System CLI.
"""
import sys
from membership_system import MembershipManager

def select_plan(manager):
    """Handles the interactive selection of a membership plan."""
    print("\nAvailable Plans:")
    plans_list = list(manager.PLAN_COSTS.items())

    for index, (plan, cost) in enumerate(plans_list, 1):
        print(f"{index}. {plan.capitalize()} (${cost})")

    while True:
        try:
            choice = int(input("\nSelect a membership plan (number): "))
            if 1 <= choice <= len(plans_list):
                return plans_list[choice - 1][0]
            print(f"Error: Please enter a number between 1 and {len(plans_list)}.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

def select_features(manager):
    """Handles the interactive selection of additional features."""
    print("\nAvailable Features:")
    features_list = list(manager.FEATURE_COSTS.items())

    for index, (feature, cost) in enumerate(features_list, 1):
        display_name = feature.replace("_", " ").capitalize()
        print(f"{index}. {display_name} (${cost})")

    print("\nEnter the numbers of the features you want to add, separated by commas (e.g., 1, 3).")
    print("If you don't want any additional features, just press Enter:")
    features_input = input("> ").strip()

    selected_features = []
    if features_input:
        input_parts = [p.strip() for p in features_input.split(",") if p.strip()]
        for part in input_parts:
            try:
                idx = int(part)
                if 1 <= idx <= len(features_list):
                    feature_key = features_list[idx - 1][0]
                    if feature_key not in selected_features:
                        selected_features.append(feature_key)
                else:
                    print(f"Warning: Number {idx} is out of range. Ignored.")
            except ValueError:
                print(f"Warning: '{part}' is not a valid number. Ignored.")
    return selected_features

def get_member_count():
    """Prompts the user for the number of members."""
    while True:
        try:
            num_members = int(input("\nEnter number of members: "))
            if num_members > 0:
                return num_members
            print("Error: Number of members must be positive.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

def main():
    """
    Main function to run the CLI application.
    Prompts user for inputs using numeric menus and displays results.
    """
    manager = MembershipManager()
    print("=== Gym Membership System ===")

    # 1. Selection
    selected_plan = select_plan(manager)
    selected_features = select_features(manager)
    num_members = get_member_count()

    # 2. Confirmation
    print("\n--- Confirmation ---")
    print(f"Plan: {selected_plan.capitalize()}")

    if selected_features:
        formatted_features = [f.replace("_", " ").capitalize() for f in selected_features]
        print(f"Features: {', '.join(formatted_features)}")
    else:
        print("Features: None")

    print(f"Members: {num_members}")

    confirm = input("\nConfirm these details? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled by user.")
        return -1

    # 3. Calculation
    total_cost = manager.calculate_cost(selected_plan, selected_features, num_members)

    if total_cost != -1:
        print(f"\nTotal Membership Cost: ${total_cost}")
        return total_cost

    print("Error calculating cost.")
    return -1

if __name__ == "__main__":
    sys.exit(main())
