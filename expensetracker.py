import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import random

# Dark Mode Colors with Neon Effects
BG_COLOR = "#0D0D0D"
TEXT_COLOR = "#39FF14"
BUTTON_COLOR = "#00FFFF"
ENTRY_BG = "#222222"
HIGHLIGHT_COLOR = "#FF00FF"

# Global Variables
user_data = {}
expense_data = {"Food": 0, "Shopping": 0, "Rent": 0, "Travel": 0}
savings = 0
reward_points = 0
previous_month_expenses = {category: random.randint(500, 5000) for category in expense_data}

# Function to create full-screen windows
def create_fullscreen_window(title):
    window = tk.Toplevel(root)
    window.title(title)
    window.configure(bg=BG_COLOR)
    window.attributes('-fullscreen', True)

    exit_button = tk.Button(window, text="❌ Exit", command=root.quit,
                            bg="red", fg="white", font=("Arial", 12, "bold"))
    exit_button.pack(side="top", anchor="ne", padx=10, pady=10)

    minimize_button = tk.Button(window, text="🔽 Minimize",
                                command=lambda: window.attributes('-fullscreen', False),
                                bg=BUTTON_COLOR, fg=BG_COLOR, font=("Arial", 12, "bold"))
    minimize_button.pack(side="top", anchor="ne", padx=10)

    return window

# Function to handle user input
def ask_details():

    def save_details():
        global user_data

        name = name_entry.get()
        mobile = mobile_entry.get()

        try:
            age = int(age_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age.")
            return

        gender = gender_var.get()

        if len(mobile) != 10 or not mobile.isdigit():
            messagebox.showerror("Error", "❌ Please enter a valid 10-digit mobile number.")
            return

        user_data = {"Name": name, "Age": age, "Gender": gender, "Mobile": mobile}

        if age < 18:
            messagebox.showinfo("Hey Kiddo!", f"🎈 Hello {name}! Let's set up your pocket money tracker!")
            details_window.destroy()
            ask_parent_details()
        else:
            occupation = occupation_var.get()
            user_data["Occupation"] = occupation

            if occupation == "Student":
                messagebox.showinfo("Yay!", "🎓 You get a special student discount on savings!")
            else:
                if not income_entry or not income_entry.get().isdigit():
                    messagebox.showerror("Error", "Please enter a valid income.")
                    return
                user_data["Income"] = int(income_entry.get())

            details_window.destroy()
            ask_expenses()

    details_window = create_fullscreen_window("Enter Your Details")

    def create_label(text):
        return tk.Label(details_window, text=text, bg=BG_COLOR, fg=TEXT_COLOR,
                        font=("Arial", 12, "bold"))

    create_label("Your Mobile Number:").pack()
    mobile_entry = ttk.Entry(details_window)
    mobile_entry.pack()

    create_label("Your Name:").pack()
    name_entry = ttk.Entry(details_window)
    name_entry.pack()

    create_label("Your Gender:").pack()
    gender_var = tk.StringVar(details_window)
    gender_var.set("Select")
    gender_menu = ttk.Combobox(details_window, textvariable=gender_var,
                              values=["Male", "Female", "Transgender"])
    gender_menu.pack()

    create_label("Your Age:").pack()
    age_entry = ttk.Entry(details_window)
    age_entry.pack()

    occupation_var = tk.StringVar(details_window)
    income_entry = None

    create_label("Your Occupation:").pack()
    occupation_menu = ttk.Combobox(details_window, textvariable=occupation_var,
                                  values=["Student", "Other"], state="readonly")
    occupation_menu.pack()

    def on_occupation_change(event):
        nonlocal income_entry
        if occupation_var.get() == "Other":
            if not income_entry:
                create_label("Your Monthly Income:").pack()
                income_entry = ttk.Entry(details_window)
                income_entry.pack()
        elif income_entry:
            income_entry.destroy()
            income_entry = None

    occupation_menu.bind("<<ComboboxSelected>>", on_occupation_change)

    submit_button = tk.Button(details_window, text="Submit", command=save_details,
                              bg=BUTTON_COLOR, fg=BG_COLOR, font=("Arial", 12, "bold"))
    submit_button.pack(pady=10)

# Parent details if under 18
def ask_parent_details():

    def save_parent_details():
        parent_number = parent_number_entry.get()
        parent_upi = parent_upi_entry.get()

        if len(parent_number) != 10 or not parent_number.isdigit():
            messagebox.showerror("Error", "Please enter a valid 10-digit parent mobile number.")
            return

        user_data["Parent Mobile"] = parent_number
        user_data["Parent UPI"] = parent_upi

        messagebox.showinfo("Great!", "Now your parents can send you pocket money easily!")
        parent_window.destroy()
        ask_expenses()

    parent_window = create_fullscreen_window("Parent Details")

    def create_label(text):
        return tk.Label(parent_window, text=text, bg=BG_COLOR, fg=TEXT_COLOR,
                        font=("Arial", 12, "bold"))

    create_label("Parent Mobile Number:").pack()
    parent_number_entry = ttk.Entry(parent_window)
    parent_number_entry.pack()

    create_label("Parent UPI ID:").pack()
    parent_upi_entry = ttk.Entry(parent_window)
    parent_upi_entry.pack()

    submit_button = tk.Button(parent_window, text="Submit", command=save_parent_details,
                              bg=BUTTON_COLOR, fg=BG_COLOR, font=("Arial", 16, "bold"))
    submit_button.pack(pady=10)

# Expense input
def ask_expenses():

    def save_expenses():
        global expense_data, savings, reward_points

        for category, entry in expense_entries.items():
            amount = entry.get()
            if amount.isdigit():
                expense_data[category] += int(amount)

        savings_amount = savings_entry.get()
        if savings_amount.isdigit():
            savings_amount = int(savings_amount)
            savings += savings_amount
            reward_points += (savings_amount // 100) * 10

        messagebox.showinfo("Saved!", "✅ Your expenses have been recorded!")

        if reward_points >= 100:
            messagebox.showinfo("Congrats!", f"🎉 You've earned {reward_points} points! Enjoy a discount coupon!")

        expense_window.destroy()
        visualize_expenses()

    expense_window = create_fullscreen_window("Track Your Expenses")

    expense_entries = {}

    for category in expense_data:
        tk.Label(expense_window, text=f"{category} Expense:",
                 bg=BG_COLOR, fg=TEXT_COLOR).pack()
        entry = ttk.Entry(expense_window)
        entry.pack()
        expense_entries[category] = entry

    tk.Label(expense_window, text="Savings This Month:",
             bg=BG_COLOR, fg=TEXT_COLOR).pack()
    savings_entry = ttk.Entry(expense_window)
    savings_entry.pack()

    submit_button = tk.Button(expense_window, text="Submit",
                              command=save_expenses,
                              bg=BUTTON_COLOR, fg=BG_COLOR,
                              font=("Arial", 12, "bold"))
    submit_button.pack(pady=10)

# Graph visualization
def visualize_expenses():
    categories = list(expense_data.keys())
    current = list(expense_data.values())
    previous = [previous_month_expenses.get(cat, 0) for cat in categories]

    x = range(len(categories))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([i - width/2 for i in x], previous, width=width, label='Previous Month', color=HIGHLIGHT_COLOR)
    plt.bar([i + width/2 for i in x], current, width=width, label='Current Month', color=BUTTON_COLOR)

    plt.xlabel('Categories')
    plt.ylabel('Amount Spent')
    plt.title('Monthly Expense Comparison')
    plt.xticks(ticks=x, labels=categories)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Main Tkinter App
root = tk.Tk()
root.title("Smart Expense Tracker")
root.configure(bg=BG_COLOR)
root.attributes('-fullscreen', True)

tk.Label(root, text="💰 Welcome to Smart Expense Tracker! 🎉",
         font=("Arial", 16, "bold"),
         bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

tk.Button(root, text="Start Tracking",
          command=ask_details,
          bg=BUTTON_COLOR, fg=BG_COLOR,
          font=("Arial", 14, "bold"),
          padx=20, pady=10).pack(pady=20)

exit_button = tk.Button(root, text="❌ Exit",
                        command=root.quit,
                        bg="red", fg="white",
                        font=("Arial", 12, "bold"))
exit_button.pack(side="bottom", pady=10)

root.mainloop()