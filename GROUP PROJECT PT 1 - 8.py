import uuid
import csv
import os
from datetime import datetime

FILENAME = "expenses.csv"

# Transaction class to represent a basic expense entry
class Transaction:
    # Initializes a new transaction with basic details
    def __init__(self, name, amount, date, category):
        self.transaction_id = str(uuid.uuid4())  # Generate a unique ID
        self.name = name
        self.amount = float(amount)
        self.date = date
        self.category = category

    # Modifies transaction details if new values are provided
    def modify(self, name=None, amount=None, date=None, category=None):
        if name:
            self.name = name
        if amount:
            self.amount = float(amount)
        if date:
            self.date = date
        if category:
            self.category = category

    # Returns a dictionary representation of the transaction
    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "name": self.name,
            "amount": self.amount,
            "date": self.date,
            "category": self.category,
            "type": "Transaction"
        }

    # Displays transaction details to the console
    def display(self):
#        print(f"ID: {self.transaction_id}")
        print(f"Name: {self.name}")
        print(f"Amount: ${self.amount:.2f}")
        print(f"Date: {self.date}")
        print(f"Category: {self.category}")


# The Classes for different categories are defined here

class MealsTransaction(Transaction):
    def __init__(self, name, category, date, amount, mealType):
        super().__init__(name, amount, date, category)
        self.mealType = mealType

    def modify(self, name=None, amount=None, date=None, category=None, mealType=None):
        super().modify(name, amount, date, category)
        if mealType is not None:
            self.mealType = mealType

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "Meal Type": self.mealType,
            "Vendor": ""  # ← optional: keeps CSV field consistent
        })
        return d

    def display(self):
        super().display()
        print(f"Meal Type: {self.mealType}")


class GroceryTransaction(Transaction):
    def __init__(self, name, category, date, amount, storeName, itemCategory):
        super().__init__(name, amount, date, category)
        self.storeName = storeName
        self.itemCategory = itemCategory

    def modify(self, name=None, amount=None, date=None, category=None, storeName=None, itemCategory=None):
        super().modify(name, amount, date, category)
        if storeName is not None:
            self.storeName = storeName
        if itemCategory is not None:
            self.itemCategory = itemCategory

    def to_dict(self):
        dictionary_data = super().to_dict()
        dictionary_data.update(
            {
            "Store Name": self.storeName,
            "Item Category": self.itemCategory
        }
        )
        return dictionary_data

    def display(self):
        super().display()
        print(f"Store Name: {self.storeName}")
        print(f"Item Category: {self.itemCategory}")

class ClothingTransaction(Transaction):
    def __init__(self, name, category, date, amount, clothingType, occasion):
        super().__init__(name, amount, date, category)
        self.clothingType = clothingType
        self.occasion = occasion

    def modify(self, name=None, amount=None, date=None, category=None, clothingType=None, occasion=None):
        super().modify(name, amount, date, category)
        if clothingType is not None:
            self.clothingType = clothingType
        if occasion is not None:
            self.occasion = occasion

    def to_dict(self):
        dictionary_data = super().to_dict()
        dictionary_data.update(
            {
                "Clothing Type": self.clothingType,
                "occasion": self.occasion
            }
        )
        return dictionary_data

    def display(self):
        super().display()
        print(f"Clothing Type: {self.clothingType}")
        print(f"occasion: {self.occasion}")

# Load transactions from CSV file
def load_transactions():
    transactions = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                t = Transaction(
                    name=row["name"],
                    amount=float(row["amount"]),
                    date=row["date"],
                    category=row["category"]
                )
                t.transaction_id = row["transaction_id"]  # Preserve the ID
                transactions.append(t)
    return transactions


# Save all transactions to CSV file (overwrite)

def save_transactions(transactions):
    with open(FILENAME, mode='w', newline='') as file:
        fieldnames = [
            "transaction_id", "name", "amount", "date", "category", "type",
            "Meal Type",
            "Store Name", "Item Category",
            "Clothing Type", "occasion"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for t in transactions:
            writer.writerow(t.to_dict())
#Function for viewing and filtering transactions defined here

def viewAndFilterTransactions(transactions):
    if not transactions:
        print("No transactions available to show.")
        print("*" * 40)
        return
    filter_choice = input("By category, date, amount, or all: ").strip().lower()

    if filter_choice == "all":
        print("\nAll Transactions:")
        for t in transactions:
            print("-" * 40)
            t.display()
        input("\nPress Enter to return to the main menu...\n")

    elif filter_choice == "category":
        available_categories = sorted(set(t.category for t in transactions))
        print("Available categories:", ", ".join(available_categories))
        filter_category = input("Enter Category: ").strip()
        print(f"\nTransactions in category '{filter_category}':")
        for t in transactions:
            if t.category.lower() == filter_category.lower():
                print("-" * 40)
                t.display()
        input("\nPress Enter to return to the main menu...\n")

    elif filter_choice == "date":
        dates = sorted(set(t.date for t in transactions))
        if dates:
            print(f"Available transaction dates: {dates[0]} to {dates[-1]}")
        else:
            print("No transaction to analyze.")
            return
        print("How would you like to view the transactions?")
        filter_date = input("Enter Date (YYYY-MM-DD): ").strip()
        print(f"\nTransactions on date '{filter_date}':")
        for t in transactions:
            if t.date == filter_date:
                print("-" * 40)
                t.display()
        input("\nPress Enter to return to the main menu...\n")

    elif filter_choice == "amount":
        amounts = sorted(set(round(t.amount, 2) for t in transactions))
        
        print("\nChoose how you want to filter amounts:")
        print("1. View top 10 highest amounts")
        print("2. View bottom 10 lowest amounts")
        print("3. View amounts above $1000")
        print("4. View amounts below $1000")

        sub_choice = input("Enter choice (1–4): ").strip()

        if sub_choice == "1":
            print("\nTop 10 Highest Amounts:")
            for amt in sorted(amounts, reverse=True)[:10]:
                print(f"  ${amt:.2f}")

        elif sub_choice == "2":
            print("\nBottom 10 Lowest Amounts:")
            for amt in amounts[:10]:
                print(f"  ${amt:.2f}")

        elif sub_choice == "3":
            print("\nTransactions with amount > $1000:")
            for t in transactions:
                if t.amount > 1000:
                    print("-" * 40)
                    t.display()

        elif sub_choice == "4":
            print("\nTransactions with amount < $1000:")
            for t in transactions:
                if t.amount < 1000:
                    print("-" * 40)
                    t.display()
        
        else:
            print("Invalid choice.")
        
        input("\nPress Enter to return to the main menu...\n")

    else:
        print("Please enter a valid choice (category, date, amount, or all).")


# Show Statistics
def show_statistics(transactions):
    if not transactions:
        print("No transactions available to show.")
        print("*" * 40)
        return

    while True:
        print("=" * 40)
        print("Expense Statistics Menu")
        print("1. Total amount by category")
        print("2. Total amount in a date range")
        print("3. Average daily expense")
        print("4. Average monthly expense")
        print("5. Back to the main menu")
        print("=" * 40)

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            totals = {}
            for t in transactions:
                if t.category in totals:
                    totals[t.category] += t.amount
                else:
                    totals[t.category] = t.amount
            print("\nTotal by Category:")
            for cat in totals:
                print(f"{cat}: ${totals[cat]:.2f}")
            input("\nPress Enter to return to the statistics menu...\n")

        elif choice == "2":
            dates = sorted(set(t.date for t in transactions))
            if dates:
                print(f"Available transaction dates: {dates[0]} to {dates[-1]}")
            else:
                print("No transaction to analyze.")
                return

            start = input("Enter start date (YYYY-MM-DD): ").strip()
            end = input("Enter end date (YYY-MM-DD): ").strip()
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                end_date = datetime.strptime(end, "%Y-%m-%d")
                total = 0
                for t in transactions:
                    transaction_date = datetime.strptime(t.date, "%Y-%m-%d")
                    if start_date <= transaction_date <= end_date:
                        total += t.amount
                    print(f"Total from {start} to {end}: ${total:.2f}")
            except ValueError:
                print("Invalid date format.")
            input("\nPress Enter to return to the statistics menu...\n")

        elif choice == "3":
            daily_totals = {}
            for t in transactions:
                if t.date in daily_totals:
                    daily_totals[t.date] += t.amount
                else:
                    daily_totals[t.date] = t.amount
            if daily_totals:
                average = sum(daily_totals.values()) / len(daily_totals)
                print(f"Average daily expense: ${average:.2f}")
            else:
                print("No Transactions found.")
            input("\nPress Enter to return to the statistics menu...\n")

        elif choice == "4":
            monthly_totals = {}
            for t in transactions:
                month = t.date[:7] #Get YYYY-MM
                if month in monthly_totals:
                    monthly_totals[month] += t.amount
                else:
                    monthly_totals[month] = t.amount
            if monthly_totals:
                average = sum(monthly_totals.values()) / len(monthly_totals)
                print(f"Average monthly expense: ${average:.2f}")
            else:
                print("No Transaction Found")
            input("\nPress Enter to return to the statistics menu...\n")

        elif choice == "5":
            break
        else:
            print("Invalid Choice. Please try again.")

# Main program function
def main():
    transactions = load_transactions()

    while True:
        print("*" * 40)
        print("Expense Manager - What would you like to do?")
        print("1. Add a transaction")
        print("2. View transactions")
        print("3. Modify a transaction")
        print("4. View Statistics")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ").strip()
        # Adding a Transaction
        if choice == "1":
            name = input("Enter expense name: ")
            amount = input("Enter amount: ")
            date = input("Enter date (YYYY-MM-DD): ")

            print("Please choose the Category. Food, Grocery, Clothing, or Other?")
            category = input("Enter category: ").strip().lower()

            if category.lower() == 'food':
                mealType = input("Enter meal type (breakfast, lunch, or dinner): ").strip()
                t = MealsTransaction(name, category, date, amount, mealType)
                transactions.append(t)
                save_transactions(transactions)
                print("Transaction added successfully!")
                input("\nPress Enter to return to the main menu...\n")

            elif category == 'grocery':

                storeName = input("Enter store name: ")
                print(storeName)
                itemCategory = input("Enter item category: ")
                print(itemCategory)

                t = GroceryTransaction(name, category, date, amount, storeName, itemCategory)
                transactions.append(t)
                save_transactions(transactions)
                print("Transaction added successfully!")
                input("\nPress Enter to return to the main menu...\n")

            elif category == 'clothing':

                clothingType = input("Enter clothing type: ")
                print(clothingType)
                occasion = input("Enter occasion: ")
                print(occasion)

                t = ClothingTransaction(name, category, date, amount, clothingType, occasion)
                transactions.append(t)
                save_transactions(transactions)
                print("Transaction added successfully!")
                input("\nPress Enter to return to the main menu...\n")

            elif category == 'other':
                t = Transaction(name, amount, date, category)
                transactions.append(t)
                save_transactions(transactions)
                print("Transaction added successfully!")
                input("\nPress Enter to return to the main menu...\n")
            else:
                print("Invalid Choice. Please try again.")

        # View and Filter Transactions

        elif choice == "2":
            if not transactions:
                print("No transactions to show.")
                continue
            else:
                viewAndFilterTransactions(transactions)

        # Modify Transactions
        elif choice == "3":
            if not transactions:
                print("No transactions available to modify.")
                print("*" * 40)
                continue

            print("\nSelect a transaction to modify:")
            for idx, t in enumerate(transactions):
                print(f"{idx + 1}. {t.name} (${t.amount:.2f}) on {t.date}")

            selection = input("Enter number: ")
            if not selection.isdigit() or int(selection) < 1 or int(selection) > len(transactions):
                print("Invalid selection.")
                continue

            selected = transactions[int(selection) - 1]
            print("\nCurrent details:")
            selected.display()

            print("\nEnter new values (press enter to keep current):")
            new_name = input(f"New name [{selected.name}]: ") or selected.name
            new_amount = input(f"New amount [{selected.amount}]: ") or selected.amount
            new_date = input(f"New date [{selected.date}]: ") or selected.date
            new_category = input(f"New category [{selected.category}]: ") or selected.category


            selected.modify(name=new_name, amount=new_amount, date=new_date, category=new_category)
            save_transactions(transactions)
            print("Transaction updated!")
            print("*" * 40)

        # Viw Statistics
        elif choice == "4":
            show_statistics(transactions)
        # Quit
        elif choice == "5":
            print("Exiting program. Goodbye!")
            print("*" * 40)
            break

        else:
            print("Invalid option. Please try again.")
            print("*" * 40)

if __name__ == "__main__":
    main()