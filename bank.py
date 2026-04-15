import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "bank_data.json"

# Load Data
def load_data():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return {}

# Save Data
def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# Create Account
def create_account():
    data = load_data()
    username = input("Enter Username: ")

    if username in data:
        print("Account already exists!")
        return

    password = input("Enter Password: ")

    data[username] = {
        "password": password,
        "balance": 0,
        "history": []
    }

    save_data(data)
    print("Account Created Successfully!")

# Login
def login():
    data = load_data()
    username = input("Username: ")
    password = input("Password: ")

    if username in data and data[username]["password"] == password:
        print("Login Successful!")
        user_menu(username)
    else:
        print("Invalid Login!")

# Deposit
def deposit(username):
    data = load_data()
    amount = int(input("Enter amount: "))

    data[username]["balance"] += amount
    data[username]["history"].append(f"Deposited {amount} {datetime.now()}")

    save_data(data)
    print("Amount Deposited!")

# Withdraw
def withdraw(username):
    data = load_data()
    amount = int(input("Enter amount: "))

    if amount > data[username]["balance"]:
        print("Insufficient Balance!")
    else:
        data[username]["balance"] -= amount
        data[username]["history"].append(f"Withdrawn {amount} {datetime.now()}")

        save_data(data)
        print("Amount Withdrawn!")

# Balance
def check_balance(username):
    data = load_data()
    print("Balance:", data[username]["balance"])

# History
def show_history(username):
    data = load_data()
    print("\nTransaction History:")
    for h in data[username]["history"]:
        print("-", h)

# Data Analysis
def analyze_data(username):
    data = load_data()
    history = data[username]["history"]

    amounts = []
    types = []

    for h in history:
        parts = h.split()
        types.append(parts[0])
        amounts.append(int(parts[1]))

    if not amounts:
        print("No transactions to analyze!")
        return

    df = pd.DataFrame({
        "Type": types,
        "Amount": amounts
    })

    print("\n📊 Total:", df["Amount"].sum())
    print("💰 Deposit:", df[df["Type"]=="Deposited"]["Amount"].sum())
    print("💸 Withdraw:", df[df["Type"]=="Withdrawn"]["Amount"].sum())

    df.groupby("Type")["Amount"].sum().plot(kind="bar")
    plt.title("Transaction Analysis")
    plt.show()

# User Menu
def user_menu(username):
    while True:
        print("\n1.Deposit 2.Withdraw 3.Balance 4.History 5.Analysis 6.Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            deposit(username)
        elif choice == "2":
            withdraw(username)
        elif choice == "3":
            check_balance(username)
        elif choice == "4":
            show_history(username)
        elif choice == "5":
            analyze_data(username)
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

# Main Menu
def main():
    while True:
        print("\n1.Create Account 2.Login 3.Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

main()