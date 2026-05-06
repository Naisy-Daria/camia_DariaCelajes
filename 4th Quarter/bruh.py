import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------- DATA ----------
subgroups = ["School", "Food", "Transportation", "Personal Expense"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

used_days = []
weekly_data = {}
current_day = None
weekly_budget = 0

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget_data.json")

last_screen = "start"

# ---------- SAVE / LOAD ----------

def save_to_file():
    data = {
        "weekly_budget": weekly_budget,
        "weekly_data": weekly_data,
        "used_days": used_days,
        "last_screen": last_screen,
        "current_day": current_day
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_from_file():
    global weekly_budget, weekly_data, used_days, last_screen, current_day

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            weekly_budget = data.get("weekly_budget", 0)
            weekly_data = data.get("weekly_data", {})
            used_days = data.get("used_days", [])
            last_screen = data.get("last_screen", "start")
            current_day = data.get("current_day", None)

# ---------- EXIT ----------
def on_close():
    save_to_file()
    root.destroy()

# ---------- RESET ----------
def reset_week():
    global used_days, weekly_data, weekly_budget, current_day, last_screen

    if messagebox.askyesno("Reset Week", "Start a new week?"):
        used_days.clear()
        weekly_data.clear()
        weekly_budget = 0
        current_day = None
        last_screen = "start"

        save_to_file()

        entry_budget.delete(0, tk.END)

        clear(main_frame)
        start_frame.pack(pady=50)

# ---------- SUMMARY TEXT ----------
def get_summary_text():
    total = sum(weekly_data.values())
    remaining = weekly_budget - total

    text = f"💰 Budget: PHP {weekly_budget:.2f}\n\n"

    if not weekly_data:
        text += "No expenses yet.\n"
    else:
        for d in weekly_data:
            text += f"{d}: PHP {weekly_data[d]:.2f}\n"

    text += f"\nTotal: PHP {total:.2f}"
    text += f"\nRemaining: PHP {remaining:.2f}"

    return text

# ---------- START ----------
def start_app():
    global weekly_budget, last_screen

    val = entry_budget.get().strip()

    if val == "":
        messagebox.showerror("Error", "Enter a budget.")
        return

    try:
        budget = float(val)

        if budget < 0:
            messagebox.showerror("Error", "Budget cannot be negative.")
            return

        weekly_budget = budget
        last_screen = "day_selection"
        save_to_file()

        start_frame.pack_forget()
        day_selection_screen()

    except ValueError:
        messagebox.showerror("Error", "Invalid number.")

# ---------- DAY SCREEN (NEW DESIGN) ----------
def day_selection_screen():
    global last_screen
    last_screen = "day_selection"
    save_to_file()

    clear(main_frame)

    main_frame.configure(bg="#f2f6ff")

    # ---------- LEFT: SUMMARY ----------
    left = tk.Frame(main_frame, bg="#dfe9ff", width=180)
    left.pack(side="left", fill="y")

    tk.Label(left, text="📊 Summary", bg="#dfe9ff",
             font=("Arial", 12, "bold")).pack(pady=10)

    summary_label = tk.Label(left, text=get_summary_text(),
                             bg="#dfe9ff", justify="left", font=("Arial", 9))
    summary_label.pack(padx=10)

    # ---------- RIGHT: DAYS ----------
    right = tk.Frame(main_frame, bg="#f2f6ff")
    right.pack(side="right", fill="both", expand=True)

    tk.Label(right, text="Select a Day",
             font=("Arial", 16, "bold"), bg="#f2f6ff").pack(pady=10)

    available_days = [d for d in days if d not in used_days]

    for d in available_days:
        tk.Button(right, text=d, width=20,
                  bg="#4a90e2", fg="white",
                  command=lambda day=d: input_screen(day)).pack(pady=3)

    tk.Button(right, text="Reset Week",
              bg="red", fg="white", width=20,
              command=reset_week).pack(pady=10)

    tk.Button(right, text="Exit",
              bg="gray", fg="white", width=20,
              command=on_close).pack()

# ---------- INPUT ----------
def input_screen(day):
    global current_day, last_screen
    current_day = day
    last_screen = "input"
    save_to_file()

    clear(main_frame)

    tk.Label(main_frame, text=f"{day} Expenses",
             font=("Arial", 14, "bold")).pack(pady=5)

    global entries
    entries = {}

    for g in subgroups:
        frame = tk.Frame(main_frame)
        frame.pack(pady=3)

        tk.Label(frame, text=g, width=18, anchor="w").pack(side="left")
        e = tk.Entry(frame)
        e.pack(side="right")

        entries[g] = e

    tk.Button(main_frame, text="Preview",
              command=preview_screen, bg="#4a90e2", fg="white").pack(pady=5)

    tk.Button(main_frame, text="Reset Week",
              command=reset_week, bg="red", fg="white").pack(pady=3)

    tk.Button(main_frame, text="Exit",
              command=on_close).pack(pady=5)

# ---------- PREVIEW ----------
def preview_screen():
    global expenses, total_spent, last_screen

    last_screen = "preview"
    save_to_file()

    expenses = {}
    total_spent = 0

    try:
        for g in subgroups:
            v = float(entries[g].get().strip())
            if v < 0:
                raise ValueError
            expenses[g] = v
            total_spent += v
    except ValueError:
        messagebox.showerror("Error", "Positive numbers only.")
        return

    clear(main_frame)

    tk.Label(main_frame, text="Preview",
             font=("Arial", 14, "bold")).pack(pady=5)

    for g in subgroups:
        tk.Label(main_frame, text=f"{g}: PHP {expenses[g]:.2f}").pack()

    tk.Label(main_frame, text=f"Total: PHP {total_spent:.2f}",
             font=("Arial", 12, "bold")).pack(pady=5)

    tk.Button(main_frame, text="Confirm & Save",
              command=save_data, bg="green", fg="white").pack(pady=3)

    tk.Button(main_frame, text="Edit",
              command=lambda: input_screen(current_day)).pack()

    tk.Button(main_frame, text="Reset Week",
              bg="red", fg="white", command=reset_week).pack(pady=3)

    tk.Button(main_frame, text="Exit",
              command=on_close).pack(pady=5)

# ---------- SAVE ----------
def save_data():
    weekly_data[current_day] = total_spent

    if current_day not in used_days:
        used_days.append(current_day)

    save_to_file()
    review_screen()

# ---------- REVIEW ----------
def review_screen():
    global last_screen
    last_screen = "review"
    save_to_file()

    clear(main_frame)

    tk.Label(main_frame, text=f"{current_day} Review",
             font=("Arial", 14, "bold")).pack(pady=5)

    for g in subgroups:
        tk.Label(main_frame, text=f"{g}: PHP {expenses[g]:.2f}").pack()

    tk.Label(main_frame, text=f"Total: PHP {total_spent:.2f}",
             font=("Arial", 12, "bold")).pack(pady=5)

    tk.Button(main_frame, text="Back to Days",
              command=day_selection_screen).pack(pady=3)

    tk.Button(main_frame, text="Reset Week",
              bg="red", fg="white", command=reset_week).pack(pady=3)

    tk.Button(main_frame, text="Exit",
              command=on_close).pack(pady=5)

# ---------- CLEAR ----------
def clear(frame):
    for w in frame.winfo_children():
        w.destroy()

# ---------- UI ----------
root = tk.Tk()
root.title("Budget Buddy")
root.geometry("600x400")

root.protocol("WM_DELETE_WINDOW", on_close)

start_frame = tk.Frame(root)
start_frame.pack(pady=50)

tk.Label(start_frame, text="Enter Weekly Budget",
         font=("Arial", 12, "bold")).pack()

entry_budget = tk.Entry(start_frame)
entry_budget.pack(pady=5)

tk.Button(start_frame, text="Start",
          command=start_app, bg="#4a90e2", fg="white").pack(pady=5)

tk.Button(start_frame, text="Reset Week",
          command=reset_week, bg="red", fg="white").pack(pady=5)

tk.Button(start_frame, text="Exit",
          command=on_close).pack()

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# ---------- LOAD ----------
load_from_file()

# ---------- RESTORE ----------
if weekly_budget == 0:
    start_frame.pack(pady=50)
else:
    start_frame.pack_forget()
    day_selection_screen()

root.mainloop()