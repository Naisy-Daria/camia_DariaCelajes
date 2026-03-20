# 1. Title
print("BUDGET TRACKER".center(50))

# Subgroups and Days
subgroups = ["School", "Food", "Transportation", "Personal Expense"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# 2. Ask for Initial Amount
initial_amount = float(input("\nEnter Initial Amount (₱): "))

# Dictionary to store expenses
expenses = {}

# 3. Ask which day
print("\nSelect Day:")
for i in range(len(days)):
    print(i + 1, "-", days[i])

day_choice = int(input("Enter day number: "))

# Validate day input
if day_choice < 1 or day_choice > len(days):
    print("Invalid day selected.")
    quit()

selected_day = days[day_choice - 1]

# 4. Input expenses for subgroups
print("\nEnter expenses for", selected_day)
for group in subgroups:
    amount = float(input("Enter amount for " + group + " (₱): "))
    expenses[group] = amount

# 5. Calculate totals
total_spent = sum(expenses.values())
remaining = initial_amount - total_spent

# 6. Display output in formatted table
print()
print("BUDGET SUMMARY".center(50))
print("Day:", selected_day)
print("Initial Amount: P {:.2f}".format(initial_amount))

print("-" * 40)
print("{:<20} {:>10}".format("Category", "Amount (P)"))
print("-" * 40)

for group in subgroups:
    print("{:<20} {:>10.2f}".format(group, expenses[group]))

print("-" * 40)
print("{:<20} {:>10.2f}".format("Total Spent", total_spent))
print("{:<20} {:>10.2f}".format("Remaining", remaining))
print("-" * 40)
