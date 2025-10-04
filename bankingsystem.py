import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import winsound
import os

FILENAME = "accounts.txt"
TRANSACTION_FILE = "transactions.txt"

def load_accounts():
    accounts = {}
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            for line in file:
                acc, name, balance = line.strip().split(",")
                accounts[acc] = [name, float(balance)]
    return accounts

def save_accounts(accounts):
    with open(FILENAME, "w") as file:
        for acc, info in accounts.items():
            file.write(f"{acc},{info[0]},{info[1]}\n")

def record_transaction(account_number, action, amount):
    with open(TRANSACTION_FILE, "a") as file:
        file.write(f"{account_number},{action},{amount}\n")

def sound_deposit(): winsound.Beep(1000, 200)
def sound_withdraw(): winsound.Beep(400, 300)

def update_balance_panel(acc):
    if acc in accounts:
        balance_label.config(text=f"Balance: {accounts[acc][1]:.2f}")
        deposit_total = 0
        withdraw_total = 0
        if os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, "r") as file:
                for line in file:
                    t_acc, action, amount = line.strip().split(",")
                    if t_acc == acc:
                        amount = float(amount)
                        if action == "Deposit":
                            deposit_total += amount
                        else:
                            withdraw_total += amount
        deposit_bar['value'] = deposit_total
        withdraw_bar['value'] = withdraw_total

def create_account():
    acc = simpledialog.askstring("Create Account", "Enter new account number:")
    if not acc: return
    if acc in accounts:
        messagebox.showerror("Error", "Account already exists!")
        return
    name = simpledialog.askstring("Create Account", "Enter account holder's name:")
    if not name: return
    accounts[acc] = [name, 0]
    save_accounts(accounts)
    messagebox.showinfo("Success", f"Account created for {name} with balance 0.")
    acc_var.set(acc)
    update_balance_panel(acc)

def deposit():
    acc = acc_var.get()
    if acc not in accounts:
        messagebox.showerror("Error", "Select a valid account!")
        return
    amount = simpledialog.askfloat("Deposit Money", "Enter amount to deposit:")
    if amount is None or amount <= 0: return
    accounts[acc][1] += amount
    save_accounts(accounts)
    record_transaction(acc, "Deposit", amount)
    sound_deposit()
    messagebox.showinfo("Success", f"Deposited {amount}. Current balance: {accounts[acc][1]}")
    update_balance_panel(acc)

def withdraw():
    acc = acc_var.get()
    if acc not in accounts:
        messagebox.showerror("Error", "Select a valid account!")
        return
    amount = simpledialog.askfloat("Withdraw Money", "Enter amount to withdraw:")
    if amount is None or amount <= 0: return
    if amount > accounts[acc][1]:
        messagebox.showerror("Error", "Insufficient balance!")
        return
    accounts[acc][1] -= amount
    save_accounts(accounts)
    record_transaction(acc, "Withdraw", amount)
    sound_withdraw()
    messagebox.showinfo("Success", f"Withdrawn {amount}. Current balance: {accounts[acc][1]}")
    update_balance_panel(acc)

def check_balance():
    acc = acc_var.get()
    if acc not in accounts:
        messagebox.showerror("Error", "Select a valid account!")
        return
    messagebox.showinfo("Balance Info", f"Account holder: {accounts[acc][0]}\nBalance: {accounts[acc][1]}")
    update_balance_panel(acc)

def view_accounts():
    if not accounts:
        messagebox.showinfo("All Accounts", "No accounts found!")
        return
    view_window = tk.Toplevel(root)
    view_window.title("All Accounts")
    view_window.geometry("450x300")
    tree = ttk.Treeview(view_window, columns=("Account", "Name", "Balance"), show="headings")
    tree.heading("Account", text="Account Number")
    tree.heading("Name", text="Name")
    tree.heading("Balance", text="Balance")
    tree.pack(fill=tk.BOTH, expand=True)
    for acc, info in accounts.items():
        tree.insert("", tk.END, values=(acc, info[0], info[1]))

def view_transactions():
    acc = acc_var.get()
    if acc not in accounts:
        messagebox.showerror("Error", "Select a valid account!")
        return
    trans_window = tk.Toplevel(root)
    trans_window.title(f"Transactions for {acc}")
    trans_window.geometry("400x300")
    tree = ttk.Treeview(trans_window, columns=("Action", "Amount"), show="headings")
    tree.heading("Action", text="Action")
    tree.heading("Amount", text="Amount")
    tree.pack(fill=tk.BOTH, expand=True)
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r") as file:
            for line in file:
                t_acc, action, amount = line.strip().split(",")
                if t_acc == acc:
                    tree.insert("", tk.END, values=(action, amount))

accounts = load_accounts()

root = tk.Tk()
root.title("🏦 Ultimate Banking System 🏦")
root.geometry("500x550")
root.config(bg="#cce6ff")

title = tk.Label(root, text="🏦 Ultimate Banking System", font=("Arial", 18, "bold"), bg="#cce6ff", fg="#003366")
title.pack(pady=15)

acc_var = tk.StringVar()
acc_label = tk.Label(root, text="Select Account:", font=("Arial", 12), bg="#cce6ff")
acc_label.pack(pady=5)
acc_menu = ttk.Combobox(root, textvariable=acc_var, values=list(accounts.keys()), state="readonly", width=25)
acc_menu.pack(pady=5)

balance_label = tk.Label(root, text="Balance: 0", font=("Arial", 14, "bold"), bg="#cce6ff", fg="#003366")
balance_label.pack(pady=10)

tk.Label(root, text="Total Deposits:", bg="#cce6ff").pack()
deposit_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", maximum=10000)
deposit_bar.pack(pady=5)

tk.Label(root, text="Total Withdrawals:", bg="#cce6ff").pack()
withdraw_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", maximum=10000)
withdraw_bar.pack(pady=5)

button_specs = [
    ("Create Account", create_account, "#3399ff"),
    ("Deposit Money", deposit, "#33cc33"),
    ("Withdraw Money", withdraw, "#ff6666"),
    ("Check Balance", check_balance, "#ffcc00"),
    ("View All Accounts", view_accounts, "#9966ff"),
    ("View Transactions", view_transactions, "#ff9900"),
    ("Exit", root.destroy, "#ff6666")
]

for text, command, color in button_specs:
    btn = tk.Button(root, text=text, font=("Arial", 12, "bold"), width=30,
                    bg=color, fg="white", activebackground="#004c99" if color=="#3399ff" else "#333333",
                    relief="raised", bd=3, command=command)
    btn.pack(pady=7)

def on_account_select(event):
    update_balance_panel(acc_var.get())
acc_menu.bind("<<ComboboxSelected>>", on_account_select)

root.mainloop()
