from tkinter import messagebox
import tkinter as tk

# Mock account data
accounts = {
    "123456789": {
        "password": "password123",
        "balance": 5000,
        "full_name": "John Doe",
        "status":"open"
    }
}

# Global variables
current_account = None
password_attempts = 0

# GUI Functions
def enter_account_number():
    global current_account

    account_number = account_entry.get()
    if account_number in accounts :
        current_account = account_number
        if accounts[current_account]["status"] == "open":
            reset_password_attempts()
            show_password_entry()
        else:
            messagebox.showerror("Error", "Account locked. Please go to the branch.")
            reset()
    else:
        messagebox.showerror("Error", "Invalid account number")
        reset()

def enter_password():
    global password_attempts

    password = password_entry.get()
    if password == accounts[current_account]["password"]:
        show_options()
    else:
        password_attempts += 1
        messagebox.showerror("Error", "Incorrect password")
        if password_attempts >= 3:
            lock_account()

def reset_password_attempts():
    global password_attempts
    password_attempts = 0

def lock_account():
    messagebox.showerror("Error", "Account locked. Please go to the branch.")
    accounts[current_account]["status"]="blocked"
    reset()

def show_password_entry():
    account_label.grid_remove()
    account_entry.grid_remove()
    enter_account_button.grid_remove()

    password_label.grid(row=0, column=0)
    password_entry.grid(row=0, column=1)
    enter_password_button.grid(row=1, column=1)

def show_options():
    password_label.grid_remove()
    password_entry.grid_remove()
    enter_password_button.grid_remove()

    cash_withdraw_button.grid(row=0, column=0)
    balance_inquiry_button.grid(row=0, column=1)
    password_change_button.grid(row=1, column=0)
    fawry_service_button.grid(row=1, column=1)
    exit_button.grid(row=2, column=0, columnspan=2)

def reset():
    account_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    account_label.grid(row=0, column=0)
    account_entry.grid(row=0, column=1)
    enter_account_button.grid(row=1, column=1)

    password_label.grid_remove()
    password_entry.grid_remove()
    enter_password_button.grid_remove()

    cash_withdraw_button.grid_remove()
    balance_inquiry_button.grid_remove()
    password_change_button.grid_remove()
    fawry_service_button.grid_remove()
    exit_button.grid_remove()

def cash_withdraw():
    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Cash Withdraw", font=("Arial", 15))

    amount_label = tk.Label(withdraw_window, text="Enter amount to withdraw (multiple of 100 L.E.):", font=("Arial", 16))
    amount_label.pack()
    amount_entry = tk.Entry(withdraw_window, font=("Arial", 16))
    amount_entry.pack()
    withdraw_button = tk.Button(withdraw_window, text="Withdraw", command=lambda: withdraw(amount_entry.get(), withdraw_window), font=("Arial", 16))
    withdraw_button.pack()

def withdraw(amount, withdraw_window):
    try:
        amount = int(amount)
        if amount % 100 != 0:
            messagebox.showerror("Error", "Not allowed value. Please enter a multiple of 100 L.E.")
        elif amount > 5000:
            messagebox.showerror("Error", "Maximum allowed value per transaction is 5000 L.E.")
        elif amount > accounts[current_account]["balance"]:
            messagebox.showerror("Error", "Insufficient balance")
        else:
            accounts[current_account]["balance"] -= amount
            #atm_actuator_out(amount)  # Call the ATM Actuator function
            messagebox.showinfo("Success", f"Withdrawal successful. Thank you for using our ATM.")
            withdraw_window.destroy()
            reset()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

def balance_inquiry():
    balance_window = tk.Toplevel(root)
    balance_window.title("Balance Inquiry")

    balance_label = tk.Label(balance_window, text=f"Account Holder: {accounts[current_account]['full_name']}\nBalance: {accounts[current_account]['balance']} L.E.", font=("Arial", 16))
    balance_label.pack()

    ok_button = tk.Button(balance_window, text="OK", command=balance_window.destroy, font=("Arial", 16))
    ok_button.pack()

def password_change():
    password_window = tk.Toplevel(root)
    password_window.title("Password Change")

    new_password_label = tk.Label(password_window, text="Enter new password (4 characters):", font=("Arial", 16))
    new_password_label.pack()
    new_password_entry = tk.Entry(password_window, show="*", font=("Arial", 16))
    new_password_entry.pack()

    confirm_password_label = tk.Label(password_window, text="Confirm new password:", font=("Arial", 16))
    confirm_password_label.pack()
    confirm_password_entry = tk.Entry(password_window, show="*", font=("Arial", 16))
    confirm_password_entry.pack()

    change_button = tk.Button(password_window, text="Change", command=lambda: change_password(new_password_entry.get(), confirm_password_entry.get(), password_window), font=("Arial", 16))
    change_button.pack()

def change_password(new_password, confirm_password, password_window):
    if len(new_password) != 4:
        messagebox.showerror("Error", "Invalid password length. Password must be 4 characters.")
    elif new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
    else:
        accounts[current_account]["password"] = new_password
        messagebox.showinfo("Success", "Password changed successfully.")
        password_window.destroy()

def fawry_service():
    fawry_window = tk.Toplevel(root)
    fawry_window.title("Fawry Service")

    fawry_options = ["Orange Recharge", "Etisalat Recharge", "Vodafone Recharge", "We Recharge"]
    fawry_variable = tk.StringVar(fawry_window)
    fawry_variable.set(fawry_options[0])
    fawry_dropdown = tk.OptionMenu(fawry_window, fawry_variable, *fawry_options)
    fawry_dropdown.pack()

    phone_label = tk.Label(fawry_window, text="Enter phone number:", font=("Arial", 16))
    phone_label.pack()
    phone_entry = tk.Entry(fawry_window, font=("Arial", 16))
    phone_entry.pack()

    amount_label = tk.Label(fawry_window, text="Enter amount:", font=("Arial", 16))
    amount_label.pack()
    amount_entry = tk.Entry(fawry_window, font=("Arial", 16))
    amount_entry.pack()

    recharge_button = tk.Button(fawry_window, text="Recharge", command=lambda: recharge(fawry_variable.get(), phone_entry.get(), amount_entry.get(), fawry_window), font=("Arial", 16))
    recharge_button.pack()

def recharge(service, phone_number, amount, fawry_window):
    # Implement the recharge functionality here
    messagebox.showinfo("Success", f"{service} recharge of {amount} L.E. for phone number {phone_number} successful.")
    fawry_window.destroy()


def show_first_page():
    # Reset the text values of the entry widgets
    account_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    # Show the widgets of the first page
    account_label.grid(row=0, column=0, padx=20, pady=10)
    account_entry.grid(row=0, column=1, padx=20, pady=10)
    enter_account_button.grid(row=1, column=1, padx=20, pady=10)

    # Hide the widgets of other pages
    password_label.grid_remove()
    password_entry.grid_remove()
    enter_password_button.grid_remove()
    cash_withdraw_button.grid_remove()
    balance_inquiry_button.grid_remove()
    password_change_button.grid_remove()
    fawry_service_button.grid_remove()
    exit_button.grid_remove()

def exit_program():
    result = messagebox.askquestion("Confirmation", "Are you sure you want to exit?")
    if result == "yes":
        root.destroy()
# Create GUI
root = tk.Tk()
icon_path = "th.ico"
root.iconbitmap(icon_path)
root.title("ATM Software")
root.geometry("600x400")
# Account Entry
account_label = tk.Label(root, text="Enter Account Number:", font=("Arial", 16))
account_label.grid(row=0, column=0)
account_entry = tk.Entry(root, font=("Arial", 16))
account_entry.grid(row=0, column=1)
enter_account_button = tk.Button(root, text="Enter", command=enter_account_number, font=("Arial", 16))

enter_account_button.grid(row=1, column=1)

# Password Entry
password_label = tk.Label(root, text="Enter Password:", font=("Arial", 24))
password_entry = tk.Entry(root, show="*", font=("Arial", 16))
enter_password_button = tk.Button(root, text="Enter", command=enter_password, font=("Arial", 16))

# Options
cash_withdraw_button = tk.Button(root, text="Cash Withdraw", command=cash_withdraw, font=("Arial", 16))
balance_inquiry_button = tk.Button(root, text="Balance Inquiry", command=balance_inquiry, font=("Arial", 16))
password_change_button = tk.Button(root, text="Password Change", command=password_change, font=("Arial", 16))
fawry_service_button = tk.Button(root, text="Fawry Service", command=fawry_service, font=("Arial", 16))
exit_button = tk.Button(root, text="Exit", command=show_first_page, font=("Arial", 14))

root.mainloop()
