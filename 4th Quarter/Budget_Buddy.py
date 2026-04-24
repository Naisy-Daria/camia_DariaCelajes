import tkinter as tk
from tkinter import messagebox

subgroups = ["School", "Food", "Transportation", "Personal Expense"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

used_days = []
weekly_data = {}
current_day = None
weekly_budget = 0

# ---------- FUNCTIONS ----------

def start_app():
    try:
        budget = float(entry_budget.get())
        if budget < 0:
            raise ValueError
        global weekly_budget
        weekly_budget = budget

        start_frame.pack_forget()
        day_selection_screen()
    except:
        messagebox.showerror("Error", "Enter a valid non-negative budget.")

def day_selection_screen():
    clear_frame(main_frame)

    tk.Label(main_frame, text="Select a Day", font=("Arial", 16)).pack(pady=10)

    available_days = [d for d in days if d not in used_days]

    # If all days are done
    if not available_days:
        tk.Label(main_frame, text="🎉 All days completed!", font=("Arial", 14)).pack(pady=10)

        total_week = sum(weekly_data.values())
        remaining = weekly_budget - total_week

        tk.Label(main_frame, text=f"Total Spent: PHP {total_week:.2f}").pack()
        tk.Label(main_frame, text=f"Remaining: PHP {remaining:.2f}").pack(pady=5)

        if remaining < 0:
            tk.Label(main_frame, text="⚠ You exceeded your budget!", fg="red").pack(pady=5)

        tk.Button(main_frame, text="Reset Week", command=reset_week,
                  fg="white", bg="red", width=20).pack(pady=5)

        tk.Button(main_frame, text="Exit", command=root.destroy,
                  fg="white", bg="black", width=20).pack(pady=5)
        return

    # Normal day selection
    for d in available_days:
        tk.Button(main_frame, text=d, width=20,
                  command=lambda day=d: input_screen(day)).pack(pady=3)

def input_screen(day):
    global current_day
    current_day = day

    clear_frame(main_frame)

    tk.Label(main_frame, text=f"{day} - Enter Expenses", font=("Arial", 14)).pack()

    global entries
    entries = {}

    for group in subgroups:
        frame = tk.Frame(main_frame)
        frame.pack(pady=2)

        tk.Label(frame, text=group, width=20, anchor="w").pack(side="left")
        e = tk.Entry(frame)
        e.pack(side="right")
        entries[group] = e

    tk.Button(main_frame, text="Preview", command=preview_screen).pack(pady=10)

def preview_screen():
    global expenses, total_spent

    expenses = {}
    total_spent = 0

    try:
        for group in subgroups:
            val = float(entries[group].get())
            if val < 0:
                raise ValueError
            expenses[group] = val
            total_spent += val
    except:
        messagebox.showerror("Error", "Enter valid non-negative numbers.")
        return

    clear_frame(main_frame)

    tk.Label(main_frame, text=f"{current_day} Preview", font=("Arial", 14)).pack()

    for g in subgroups:
        tk.Label(main_frame, text=f"{g}: PHP {expenses[g]:.2f}").pack()

    tk.Label(main_frame, text=f"Total: PHP {total_spent:.2f}").pack(pady=5)

    tk.Button(main_frame, text="Confirm & Save", command=save_data).pack(pady=3)
    tk.Button(main_frame, text="Edit", command=lambda: input_screen(current_day)).pack(pady=3)

def save_data():
    weekly_data[current_day] = total_spent
    if current_day not in used_days:
        used_days.append(current_day)

    review_screen()

def review_screen():
    clear_frame(main_frame)

    tk.Label(main_frame, text=f"{current_day} Review", font=("Arial", 14)).pack()

    for g in subgroups:
        tk.Label(main_frame, text=f"{g}: PHP {expenses[g]:.2f}").pack()

    tk.Label(main_frame, text=f"Total: PHP {total_spent:.2f}").pack(pady=5)

    tk.Button(main_frame, text="Finalize", command=final_summary).pack(pady=3)
    tk.Button(main_frame, text="Edit Again", command=lambda: input_screen(current_day)).pack(pady=3)

def final_summary():
    clear_frame(main_frame)

    total_week = sum(weekly_data.values())
    remaining = weekly_budget - total_week

    tk.Label(main_frame, text=f"{current_day} Summary", font=("Arial", 14)).pack()

    for g in subgroups:
        tk.Label(main_frame, text=f"{g}: PHP {expenses[g]:.2f}").pack()

    tk.Label(main_frame, text=f"Total: PHP {total_spent:.2f}").pack()

    if remaining < 0:
        tk.Label(main_frame, text="⚠ Exceeded Budget!", fg="red").pack()
    else:
        tk.Label(main_frame, text=f"Remaining: PHP {remaining:.2f}").pack()

    tk.Button(main_frame, text="Next Day", command=day_selection_screen).pack(pady=5)

def weekly_summary():
    clear_frame(main_frame)

    tk.Label(main_frame, text="Weekly Summary", font=("Arial", 14)).pack()

    total_week = sum(weekly_data.values())
    remaining = weekly_budget - total_week

    for d in weekly_data:
        tk.Label(main_frame, text=f"{d}: PHP {weekly_data[d]:.2f}").pack()

    tk.Label(main_frame, text=f"Total: PHP {total_week:.2f}").pack()
    tk.Label(main_frame, text=f"Remaining: PHP {remaining:.2f}").pack()

    tk.Button(main_frame, text="Back", command=day_selection_screen).pack(pady=5)

def reset_week():
    global used_days, weekly_data, current_day, weekly_budget
    
    confirm = messagebox.askyesno("Reset Week", "Are you sure you want to reset all data?")
    
    if confirm:
        used_days.clear()
        weekly_data.clear()
        current_day = None
        weekly_budget = 0
        
        entry_budget.delete(0, tk.END)
        
        clear_frame(main_frame)
        start_frame.pack(pady=50)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# ---------- UI SETUP ----------

root = tk.Tk()
root.title("Budget Buddy")
root.geometry("400x500")

start_frame = tk.Frame(root)
start_frame.pack(pady=50)

tk.Label(start_frame, text="Enter Weekly Budget (PHP)", font=("Arial", 12)).pack()
entry_budget = tk.Entry(start_frame)
entry_budget.pack(pady=5)

tk.Button(start_frame, text="Start", command=start_app).pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

root.mainloop()
