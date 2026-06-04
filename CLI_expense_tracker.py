import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Entertainment", "Other"]

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

def print_header(title):
    print("\n")
    print(f"  {title}")

def print_table(expenses):
    if not expenses:
        print("  No expenses to show.")
        return

    col = {"no": 4, "date": 12, "category": 15, "amount": 10, "note": 20}

    header = (
        f"  {'#':<{col['no']}}"
        f"{'Date':<{col['date']}}"
        f"{'Category':<{col['category']}}"
        f"{'Amount (₹)':>{col['amount']}}"
        f"  {'Note'}"
    )
    print(header)
    total = 0.0
    for i, exp in enumerate(expenses, start=1):
        note = exp["note"] if exp["note"] else "—"
        # Truncate long notes
        if len(note) > 22:
            note = note[:19] + "..."
        print(
            f"  {i:<{col['no']}}"
            f"{exp['date']:<{col['date']}}"
            f"{exp['category']:<{col['category']}}"
            f"{exp['amount']:>{col['amount']}.2f}"
            f"  {note}"
        )
        total += exp["amount"]

    print(f"  {'TOTAL':>{col['no'] + col['date'] + col['category']}}"
          f"{total:>{col['amount']}.2f}")

def get_valid_amount():
    while True:
        raw = input("  Amount (₹): ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print(" Amount must be greater than 0. Try again.")
            else:
                return round(amount, 2)
        except ValueError:
            print("  Invalid amount. Enter a number (e.g. 150 or 49.99).")


def get_valid_category():
    print("  Categories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"    [{i}] {cat}")
    while True:
        choice = input("  Choose category (1-4): ").strip()
        if choice in [str(i) for i in range(1, len(CATEGORIES) + 1)]:
            return CATEGORIES[int(choice) - 1]
        print("  Invalid choice. Enter a number between 1 and 4.")


def add_expense(expenses):
    print_header("ADD EXPENSE")

    amount = get_valid_amount()
    category = get_valid_category()
    note = input("  Note (optional, press Enter to skip): ").strip()

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "amount": amount,
        "note": note,
    }

    expenses.append(expense)
    save_expenses(expenses)

    print(f"\n  Expense of ₹{amount:.2f} ({category}) saved successfully!")

def view_all_expenses(expenses):
    print_header("ALL EXPENSES")
    if not expenses:
        print("  No expenses recorded yet. Add one first!")
        return
    print(f"  Showing {len(expenses)} expense:\n")
    print_table(expenses)


def filter_by_category(expenses):
    print_header("FILTER BY CATEGORY")

    if not expenses:
        print("  No expenses recorded yet. Add one first!")
        return

    print("  Filter by:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"    [{i}] {cat}")

    choice = input("  Choose category (1-4): ").strip()
    if choice not in [str(i) for i in range(1, len(CATEGORIES) + 1)]:
        print("  Invalid choice.")
        return

    selected = CATEGORIES[int(choice) - 1]
    filtered = [e for e in expenses if e["category"] == selected]

    print(f"\n  Expenses in '{selected}':\n")
    print_table(filtered)

    if not filtered:
        print(f"  No expenses found in '{selected}'.")


def print_menu():
    print("  EXPENSE TRACKER  —  What would you like to do?")
    print("\n")
    print("  [1]  Add an expense")
    print("  [2]  View all expenses")
    print("  [3]  Filter by category")
    print("  [4]  Quit")
    print("\n")

def main():
    print("\n")
    print("  CLI PERSONAL EXPENSE TRACKER")
    print("\n")

    expenses = load_expenses()
    print(f"\n  Loaded {len(expenses)} existing expense(s) from '{DATA_FILE}'.")

    menu_actions = {
        "1": lambda: add_expense(expenses),
        "2": lambda: view_all_expenses(expenses),
        "3": lambda: filter_by_category(expenses),
    }

    while True:
        print_menu()
        choice = input("  Enter choice: ").strip()

        if choice in menu_actions:
            menu_actions[choice]()
        elif choice == "4":
            print("\n Saved.\n")
            break
        else:
            print(" Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
