import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook

# Helper Functions

def load_data(filename='finance_data.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            if 'deposits' not in data:
                data['deposits'] = []
            return data
    return {'income': [], 'expenses': [], 'deposits': [], 'balance': 0}

def save_data(data, filename='finance_data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def add_income(data, amount, category):
    income_entry = {
        'amount': amount,
        'category': category,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data['income'].append(income_entry)
    data['balance'] += amount
    save_data(data)
    messagebox.showinfo("Success", "Income added successfully.")

def add_expense(data, amount, category):
    expense_entry = {
        'amount': amount,
        'category': category,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data['expenses'].append(expense_entry)
    data['balance'] -= amount
    save_data(data)
    messagebox.showinfo("Success", "Expense added successfully.")

def add_deposit(data, amount, bank_name):
    deposit_entry = {
        'amount': amount,
        'bank_name': bank_name,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data['deposits'].append(deposit_entry)
    data['balance'] += amount
    save_data(data)
    messagebox.showinfo("Success", "Bank deposit added successfully.")

def view_balance(data):
    balance_message = f"Current Balance: {data['balance']}"
    messagebox.showinfo("Balance", balance_message)

def view_income_summary(data):
    summary_by_date = {}
    for income in data['income']:
        date = income['date'].split(' ')[0]
        category = income.get('category', 'Uncategorized')
        amount = income['amount']
        if date not in summary_by_date:
            summary_by_date[date] = {}
        if category not in summary_by_date[date]:
            summary_by_date[date][category] = 0
        summary_by_date[date][category] += amount

    summary_message = "Income Summary by Date and Category:\n\n"
    for date, categories in summary_by_date.items():
        summary_message += f"Date: {date}\n"
        summary_message += "Category         | Amount\n"
        summary_message += "-----------------|--------\n"
        for category, amount in categories.items():
            summary_message += f"{category:<16} | {amount}\n"
        summary_message += "\n"
    
    messagebox.showinfo("Income Summary", summary_message)

def view_expense_summary(data):
    summary_by_date = {}
    for expense in data['expenses']:
        date = expense['date'].split(' ')[0]
        category = expense.get('category', 'Uncategorized')
        amount = expense['amount']
        if date not in summary_by_date:
            summary_by_date[date] = {}
        if category not in summary_by_date[date]:
            summary_by_date[date][category] = 0
        summary_by_date[date][category] += amount

    summary_message = "Expense Summary by Date and Category:\n\n"
    for date, categories in summary_by_date.items():
        summary_message += f"Date: {date}\n"
        summary_message += "Category         | Amount\n"
        summary_message += "-----------------|--------\n"
        for category, amount in categories.items():
            summary_message += f"{category:<16} | {amount}\n"
        summary_message += "\n"
    
    messagebox.showinfo("Expense Summary", summary_message)

def view_deposit_summary(data):
    summary_by_date = {}
    for deposit in data['deposits']:
        date = deposit['date'].split(' ')[0]
        category = deposit.get('bank_name', 'Uncategorized')
        amount = deposit['amount']
        if date not in summary_by_date:
            summary_by_date[date] = {}
        if category not in summary_by_date[date]:
            summary_by_date[date][category] = 0
        summary_by_date[date][category] += amount

    summary_message = "Deposit Summary by Date and Category:\n\n"
    for date, categories in summary_by_date.items():
        summary_message += f"Date: {date}\n"
        summary_message += "Bank         | Amount\n"
        summary_message += "-----------------|--------\n"
        for category, amount in categories.items():
            summary_message += f"{category:<16} | {amount}\n"
        summary_message += "\n"
    
    messagebox.showinfo("Deposit Summary", summary_message)

    




# New function to clear all data
def clear_all_data():
    data = {'income': [], 'expenses': [], 'deposits': [], 'balance': 0}
    save_data(data)
    messagebox.showinfo("Clear All", "All data has been cleared.")

# New function to export data to Excel
def export_to_excel(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Finance Summary"

    # Add headers for each section
    sheet.append(["Date", "Category/Bank", "Amount", "Type"])
    
    # Populate income entries
    for income in data['income']:
        sheet.append([income['date'], income['category'], income['amount'], "Income"])

    # Populate expense entries
    for expense in data['expenses']:
        sheet.append([expense['date'], expense['category'], expense['amount'], "Expense"])

    # Populate deposit entries
    for deposit in data['deposits']:
        sheet.append([deposit['date'], deposit['bank_name'], deposit['amount'], "Deposit"])

    # Add balance row
    sheet.append(["", "", "", ""])
    sheet.append(["", "Total Balance", data['balance'], ""])

    # Save the workbook
    filename = f"Finance_Summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    workbook.save(filename)
    messagebox.showinfo("Excel Export", f"Data exported successfully to {filename}")

# Tkinter Interface Setup
def main():
    data = load_data()

    # Initialize the main window
    root = tk.Tk()
    root.title("Personal Finance Tracker")
    root.geometry("700x400")

    # Create frames for left and right sections
    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
    
    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    # Function to add income with validation and clearing fields
    def add_income_ui():
        try:
            amount = float(entry_income_amount.get())
            category = entry_income_category.get()
            add_income(data, amount, category)
            entry_income_amount.delete(0, tk.END)
            entry_income_category.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")

    # Function to add expense with validation and clearing fields
    def add_expense_ui():
        try:
            amount = float(entry_expense_amount.get())
            category = entry_expense_category.get()
            add_expense(data, amount, category)
            entry_expense_amount.delete(0, tk.END)
            entry_expense_category.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")

    # Function to add bank deposit with validation and clearing fields
    def add_deposit_ui():
        try:
            amount = float(entry_deposit_amount.get())
            bank_name = entry_deposit_bank.get()
            add_deposit(data, amount, bank_name)
            entry_deposit_amount.delete(0, tk.END)
            entry_deposit_bank.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")

    # Add Income Section in left frame
    tk.Label(left_frame, text="Add Income").pack()
    tk.Label(left_frame, text="Amount").pack()
    entry_income_amount = tk.Entry(left_frame)
    entry_income_amount.pack()
    tk.Label(left_frame, text="Category").pack()
    entry_income_category = tk.Entry(left_frame)
    entry_income_category.pack()
    tk.Button(left_frame, text="Add Income", command=add_income_ui).pack(pady=10)

    # Add Expense Section in left frame
    tk.Label(left_frame, text="Add Expense").pack()
    tk.Label(left_frame, text="Amount").pack()
    entry_expense_amount = tk.Entry(left_frame)
    entry_expense_amount.pack()
    tk.Label(left_frame, text="Category").pack()
    entry_expense_category = tk.Entry(left_frame)
    entry_expense_category.pack()
    tk.Button(left_frame, text="Add Expense", command=add_expense_ui).pack(pady=10)

    # Add Bank Deposit Section in left frame
    tk.Label(left_frame, text="Add Bank Deposit").pack()
    tk.Label(left_frame, text="Amount").pack()
    entry_deposit_amount = tk.Entry(left_frame)
    entry_deposit_amount.pack()
    tk.Label(left_frame, text="Bank Name").pack()
    entry_deposit_bank = tk.Entry(left_frame)
    entry_deposit_bank.pack()
    tk.Button(left_frame, text="Add Deposit", command=add_deposit_ui).pack(pady=10)

    # View Balance and Summaries in right frame
    tk.Button(right_frame, text="View Balance", command=lambda: view_balance(data)).pack(pady=5, anchor="center", expand=True, fill='x')
    tk.Button(right_frame, text="View Income Summary", command=lambda: view_income_summary(data)).pack(pady=5, anchor="center", expand=True, fill='x')
    tk.Button(right_frame, text="View Expense Summary", command=lambda: view_expense_summary(data)).pack(pady=5, anchor="center", expand=True, fill='x')
    tk.Button(right_frame, text="View Deposit Summary", command=lambda: view_deposit_summary(data)).pack(pady=5, anchor="center", expand=True, fill='x')

    # Clear All and Export to Excel buttons
    tk.Button(right_frame, text="Clear All", command=clear_all_data).pack(pady=15, anchor="center", expand=True, fill='x')
    tk.Button(right_frame, text="Export to Excel", command=lambda: export_to_excel(data)).pack(pady=5, anchor="center", expand=True, fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()
