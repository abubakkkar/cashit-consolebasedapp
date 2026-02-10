import time
import json
import os
from datetime import datetime

# ---------------- ACCOUNT DATABASE ----------------

def get_default_users():
    return {
        # -------- ADMIN --------
        "00000-0000000-0": {
            "name": "ADMIN",
            "cnic": "00000-0000000-0",
            "iban": None,
            "pin": "0000",
            "balance": 0.0,
            "savings": 0.0,
            "monthly_spending": 0.0,
            "transactions": []
        },

        "35202-9823471-2": {
            "name": "Muhammad Ali",
            "cnic": "35202-9823471-2",
            "iban": "PK11 1111 1111 1111 1111",
            "pin": "1234",
            "balance": 1245500.00,
            "savings": 450000.00,
            "monthly_spending": 85200.00,
            "transactions": [
                ("Netflix Subscription", "Dec 02, 2025", "-1500"),
                ("Salary Credit", "Dec 01, 2025", "+350000"),
                ("Carrefour Grocery", "Nov 28, 2025", "-24350"),
                ("LESCO Bill", "Nov 25, 2025", "-18200"),
            ]
        },

        "35202-9876543-1": {
            "name": "Sara Imran",
            "cnic": "35202-9876543-1",
            "iban": "PK33 3333 3333 3333 3333",
            "pin": "9999",
            "balance": 965200.00,
            "savings": 42000.00,
            "monthly_spending": 32200.00,
            "transactions": [
                ("UET Fee", "Dec 22, 2025", "-100500"),
                ("Salary Credit", "Dec 20, 2025", "+350000"),
                ("Chezious Bill", "Dec 19, 2025", "-4350"),
                ("Income Tax", "Dec 25, 2025", "-3200"),
            ]
        },

        "35202-1234567-9": {
            "name": "Ahmed Khan",
            "cnic": "35202-1234567-9",
            "iban": "PK22 2222 2222 2222 2222",
            "pin": "5678",
            "balance": 132500.00,
            "savings": 20000.00,
            "monthly_spending": 5200.00,
            "transactions": [
                ("Gas Bill", "Dec 21, 2025", "-1500"),
                ("Salary Credit", "Dec 14, 2025", "+50000"),
                ("PTCL Bill", "Dec 11, 2025", "-2350"),
                ("E-Challan", "Dec 05, 2025", "-2000"),
            ]
        }
    }

# File handling setup
DATA_FILE = "users.json"

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            USERS = json.load(f)
        # Ensure numeric fields are floats
        for user in USERS.values():
            user["balance"] = float(user["balance"])
            user["savings"] = float(user["savings"])
            user["monthly_spending"] = float(user["monthly_spending"])
        print("✓ Previous accounts loaded successfully!\n")
    except:
        print("⚠️  Saved file corrupted or invalid. Starting with default accounts.\n")
        USERS = get_default_users()
else:
    print("👋 First time running — starting with default accounts.\n")
    USERS = get_default_users()

def save_users():
    """Save all user data to file"""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(USERS, f, indent=4)
    except Exception as e:
        print(f"❌ Failed to save data: {e}")

# ---------------- VALIDATION FUNCTIONS ----------------

def is_all_digits(text):
    for char in text:
        if char < '0' or char > '9':
            return False
    return True

def validate_cnic(cnic):
    cnic = cnic.strip()
    
    if cnic.count('-') != 2:
        return False
    
    parts = cnic.split('-')
    
    if len(parts) != 3:
        return False
    
    part1 = parts[0]
    part2 = parts[1]
    part3 = parts[2]
    
    if len(part1) != 5 or len(part2) != 7 or len(part3) != 1:
        return False
    
    if not (is_all_digits(part1) and is_all_digits(part2) and is_all_digits(part3)):
        return False
    
    return True

def validate_iban(iban):
    clean = iban.replace(" ", "").upper()
    
    if not clean.startswith("PK"):
        return False
    
    if len(clean) < 22 or len(clean) > 26:
        return False
    
    rest = clean[2:]
    for char in rest:
        if not ('0' <= char <= '9'):
            return False
            
    return True

def validate_pin(pin):
    pin = pin.strip()
    
    if len(pin) != 4:
        return False
        
    return is_all_digits(pin)

# ---------------- CREATE ACCOUNT ----------------
def create_account():
    print("\n" + "="*50)
    print("          CREATE NEW ACCOUNT          ")
    print("="*50)
    print("Welcome! Please provide the required information")
    print("to open your new bank account with us.")
    print("="*50 + "\n")

    # CNIC Input and Validation
    while True:
        print("CNIC Format Example: 12345-6789012-3")
        cnic = input("\nEnter your CNIC: ").strip()
        
        if cnic == "":
            print("❌ CNIC cannot be empty. Please try again.\n")
            continue
        
        if not validate_cnic(cnic):
            print("❌ Invalid CNIC format.")
            print("   • Must be in format: XXXXX-XXXXXXX-X")
            print("   • All parts must be digits only")
            print("   • No extra spaces or characters allowed\n")
            continue
        
        if cnic in USERS:
            print("❌ An account with this CNIC already exists.")
            print("   If this is your account, please login instead.\n")
            continue
        
        print("✓ CNIC is valid and available.\n")
        break

    # Full Name Input
    while True:
        name = input("Enter your Full Name: ").strip()
        
        if name == "":
            print("❌ Name cannot be empty.\n")
            continue
        
        if len(name) < 3:
            print("❌ Name is too short. Please enter your full name.\n")
            continue
        
        if any(char.isdigit() for char in name):
            print("❌ Name should not contain numbers.\n")
            continue
        
        print(f"✓ Name accepted: {name}\n")
        break

    # IBAN Input and Validation
    print("IBAN Format Example: PK11456345687908765439")
    print("   • Must start with 'PK'")
    print("   • Total length (without spaces): 22 to 26 characters")
    print("   • Only numbers and spaces allowed\n")
    
    while True:
        iban = input("Enter your IBAN: ").strip()
        
        if iban == "":
            print("❌ IBAN cannot be empty.\n")
            continue
        
        if not validate_iban(iban):
            print("❌ Invalid IBAN format.")
            print("   Please check and re-enter your full IBAN correctly.\n")
            continue
        
        print("✓ IBAN is valid.\n")
        break

    # PIN Input and Validation
    print("Security PIN Information:")
    print("   • Must be exactly 4 digits")
    print("   • Used for login and transaction confirmation")
    print("   • Choose a secure PIN (avoid 0000, 1234, etc.)\n")
    
    while True:
        pin = input("Set your 4-digit PIN: ").strip()
        
        if pin == "":
            print("❌ PIN cannot be empty.\n")
            continue
        
        if not validate_pin(pin):
            print("❌ PIN must be exactly 4 digits long and contain only numbers.\n")
            continue
        
        weak_pins = ["0000", "1234", "1111", "2222", "9999", "9876", "5678"]
        if pin in weak_pins:
            print("⚠️  Warning: This is a commonly used PIN and may not be secure.")
        
        confirm_pin = input("Confirm your PIN: ").strip()
        
        if confirm_pin != pin:
            print("❌ PINs do not match. Please try again.\n")
            continue
        
        print("✓ PIN set successfully.\n")
        break

    # Create the account dictionary
    USERS[cnic] = {
        "name": name.title(),                   
        "cnic": cnic,
        "iban": iban.upper().replace(" ", ""),    
        "pin": pin,
        "balance": 500.0,
        "savings": 0.0,
        "monthly_spending": 0.0,
        "transactions": []
    }

    save_users() 

    # Success Message
    print("="*50)
    print("           ACCOUNT CREATED SUCCESSFULLY!           ")
    print("="*50)
    print(f"   Welcome, {name.title()}!")
    print(f"   Account CNIC: {cnic}")
    print(f"   You got bonus Rs.500!")
    print(f"   Your account is now active and ready to use.")
    print("="*50)
    print("🎉 Thank you for banking with us!\n")

# ---------------- LOGIN ----------------

def login():
    print("\n===============================")
    print("         CASHIT LOGIN")
    print("===============================\n")

    while True:
        cnic = input("Enter CNIC (XXXXX-XXXXXXX-X): ").strip()
        pin = input("Enter 4-digit PIN: ").strip()

        if not validate_cnic(cnic):
            print("❌ Invalid CNIC Format.\n")
            continue

        if not validate_pin(pin):
            print("❌ PIN Must be 4 digits.\n")
            continue

        if cnic in USERS:
            acc = USERS[cnic]
            if acc["pin"] == pin:
                print("\n✅ Login Successful!\n")
                time.sleep(1)
                return acc
            else:
                print("❌ Incorrect PIN.\n")
        else:
            print("❌ No account found.\n")

        retry = input("Try again? (yes/no): ").lower()
        if retry != "yes":
            exit()

# ---------------- DASHBOARD ----------------

def show_dashboard(acc):
    print("\n" + "="*60)
    print("             DASHBOARD OVERVIEW             ")
    print("="*60 + "\n")

    print(f"👤 Account Holder : {acc['name']}")
    print(f"🆔 CNIC           : {acc['cnic']}")
    print(f"🏦 IBAN           : {acc['iban']}\n")

    print(f"💰 Current Balance    : Rs {acc['balance']:,.2f}")
    print(f"💼 Savings Account    : Rs {acc['savings']:,.2f}")
    print(f"📉 Monthly Spending   : Rs {acc['monthly_spending']:,.2f}\n")

    print("📌 Recent Transactions (Last 5):")
    print("-" * 60)

    if len(acc["transactions"]) == 0:
        print("   No transactions recorded yet.\n")
    else:
        for t in acc["transactions"][-5:]:
            if isinstance(t, (tuple, list)):
                if len(t) >= 3:
                    description = t[0]
                    date = t[1]
                    amount = t[2]
                else:
                    description = str(t)
                    date = "Unknown Date"
                    amount = "N/A"
                time_display = ""
            else:
                description = t.get("description", "Unknown")
                date = t.get("date", "Unknown Date")
                time_display = t.get("time", "")
                amount = t.get("amount", "N/A")

            try:
                amount_clean = str(amount).replace("Rs", "").replace("+", "").replace("-", "").strip()
                amount_float = float(amount_clean)
                sign = "+" if "+" in str(amount) else "-"
                amount_display = f"{sign}Rs {amount_float:,.2f}"
            except:
                amount_display = amount

            if time_display:
                print(f"   {description}")
                print(f"      {date} at {time_display} → {amount_display}")
            else:
                print(f"   {description} | {date} → {amount_display}")

            print("   " + "-" * 50)

    print("="*60 + "\n")

# ---------------- ADMIN DASHBOARD ----------------

def admin_dashboard():
    while True:
        print("\n===============================")
        print("        ADMIN DASHBOARD")
        print("===============================\n")

        print("1. View All Users")
        print("2. Delete User")
        print("3. Add / Deduct Money")
        print("4. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            for cnic, user in USERS.items():
                print("\n----------------------------")
                print(f"Name: {user['name']}")
                print(f"CNIC: {cnic}")
                print(f"IBAN: {user['iban']}")
                print(f"Balance: Rs {user['balance']:,}")

        elif choice == "2":
            del_cnic = input("Enter CNIC to delete: ").strip()

            if del_cnic == "00000-0000000-0":
                print("❌ Cannot delete ADMIN.")
            elif del_cnic in USERS:
                del USERS[del_cnic]
                save_users()
                print("✅ User deleted successfully.")
            else:
                print("❌ User not found.")

        elif choice == "3":
            admin_adjust_balance()

        elif choice == "4":
            print("\nAdmin Logged Out.")
            break

        else:
            print("❌ Invalid Option.")

    
# ---------------- PAYMENT FUNCTIONS ----------------

def deduct_balance(acc, amount):
    print("\n" + "-"*40)
    print("         CHECKING BALANCE         ")
    print("-"*40)
    
    current_balance = acc["balance"]
    print(f"Your Current Balance: Rs {current_balance:,.2f}")
    print(f"Requested Deduction : Rs {amount:,.2f}")
    
    if current_balance < amount:
        print("\n❌ Insufficient Balance!")
        print("   Transaction cannot be processed.")
        print("   Please deposit funds or enter a smaller amount.\n")
        return False
    
    acc["balance"] -= amount
    save_users()  # Save updated balance
    
    print(f"\n✓ Amount Deducted Successfully.")
    print(f"New Balance: Rs {acc['balance']:,.2f}\n")
    return True

def add_transaction(acc, description, amount, transaction_type="debit"):
    current_date = datetime.now().strftime("%b %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    transaction_entry = {
        "description": description,
        "date": current_date,
        "time": current_time,
        "amount": f"-{amount:,.2f}",
        "type": transaction_type,
        "balance_after": acc["balance"]
    }
    
    acc["transactions"].append(transaction_entry)
    save_users()  # Save new transaction
    
    print("✓ Transaction Recorded Successfully.")
    print(f"   Description: {description}")
    print(f"   Date       : {current_date} at {current_time}")
    print(f"   Amount     : Rs -{amount:,.2f}\n")

# [transfer_payment, bill_payment, tax_payment, challan_payment remain exactly the same as your original]

def transfer_payment(acc):
    print("\n" + "="*50)
    print("             MONEY TRANSFER             ")
    print("="*50)
    
    while True:
        iban = input("\nEnter Receiver's IBAN (e.g., PK12ABCD...): ").strip()
        
        if iban == "":
            print("❌ IBAN cannot be empty.\n")
            continue
        
        if len(iban.replace(" ", "")) < 10:
            print("❌ IBAN seems too short. Please enter the full IBAN.\n")
            continue
        
        clean_iban = iban.replace(" ", "").upper()
        if not clean_iban.startswith("PK"):
            print("⚠️  Warning: IBAN should start with 'PK' for Pakistani accounts.\n")
        
        confirm = input(f"Confirm transfer to IBAN: {iban} ? (y/n): ").lower()
        if confirm in ['y', 'yes']:
            break
        else:
            print("Transfer cancelled. Please re-enter IBAN.\n")
    
    while True:
        try:
            amount_input = input("Enter Amount to Transfer (Rs): ").strip()
            if amount_input == "":
                print("❌ Amount cannot be empty.\n")
                continue
            
            amount = float(amount_input)
            
            if amount <= 0:
                print("❌ Amount must be greater than zero.\n")
                continue
            
            if amount > 1000000: 
                print("⚠️  Large amount detected.")
                confirm_large = input("Are you sure you want to transfer this amount? (y/n): ").lower()
                if confirm_large not in ['y', 'yes']:
                    print("Transaction cancelled.\n")
                    return
            
            break
        
        except ValueError:
            print("❌ Invalid amount. Please enter numbers only (e.g., 5000.50).\n")
    
    print(f"\nSummary:")
    print(f"   Receiver IBAN : {iban}")
    print(f"   Amount        : Rs {amount:,.2f}")
    
    final_confirm = input("\nConfirm Transfer? (y/n): ").lower()
    if final_confirm not in ['y', 'yes']:
        print("\n❌ Transfer Cancelled by User.\n")
        return
    
    if deduct_balance(acc, amount):
        short_iban = iban[:10] + "..." + iban[-4:] if len(iban) > 14 else iban
        add_transaction(acc, f"Transfer to {short_iban}", amount, "transfer")
        
        print("="*50)
        print("     🎉 TRANSFER SUCCESSFUL!     ")
        print("="*50)
        print(f"   Rs {amount:,.2f} has been transferred to")
        print(f"   IBAN: {iban}")
        print("   Thank you for using our service!\n")

# The other payment functions (bill, tax, challan) are unchanged — they already call deduct_balance and add_transaction, so they are automatically saved.

def bill_payment(acc):
    print("\n" + "="*50)
    print("             BILL PAYMENT               ")
    print("="*50)
    
    print("Supported Bills: Electricity, Gas, Water, Internet, Mobile, etc.\n")
    
    while True:
        bill_id = input("Enter Bill Reference/ID (e.g., Consumer Number): ").strip()
        if bill_id == "":
            print("❌ Bill ID cannot be empty.\n")
            continue
        break
    
    while True:
        try:
            amount_input = input(f"Enter Bill Amount (Rs): ").strip()
            amount = float(amount_input)
            if amount <= 0:
                print("❌ Amount must be greater than zero.\n")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid amount (numbers only).\n")
    
    print(f"\nBill Payment Summary:")
    print(f"   Bill ID/Reference : {bill_id}")
    print(f"   Amount            : Rs {amount:,.2f}")
    
    confirm = input("\nProceed with Payment? (y/n): ").lower()
    if confirm not in ['y', 'yes']:
        print("\n❌ Bill Payment Cancelled.\n")
        return
    
    if deduct_balance(acc, amount):
        add_transaction(acc, f"Bill Payment - ID {bill_id}", amount, "bill")
        
        print("="*50)
        print("     🎉 BILL PAYMENT SUCCESSFUL!     ")
        print("="*50)
        print(f"   Bill ID: {bill_id}")
        print(f"   Amount Paid: Rs {amount:,.2f}")
        print("   Your bill has been paid successfully.\n")

def tax_payment(acc):
    print("\n" + "="*50)
    print("              TAX PAYMENT               ")
    print("="*50)
    
    print("Pay your Income Tax, Sales Tax, Property Tax, etc.\n")
    
    while True:
        tax_id = input("Enter Tax Reference Number / NTN / CPR: ").strip()
        if tax_id == "":
            print("❌ Tax reference cannot be empty.\n")
            continue
        break
    
    while True:
        try:
            amount_input = input("Enter Tax Amount (Rs): ").strip()
            amount = float(amount_input)
            if amount <= 0:
                print("❌ Amount must be greater than zero.\n")
                continue
            break
        except ValueError:
            print("❌ Invalid amount entered.\n")
    
    print(f"\nTax Payment Details:")
    print(f"   Reference No: {tax_id}")
    print(f"   Amount      : Rs {amount:,.2f}")
    
    confirm = input("\nConfirm Tax Payment? (y/n): ").lower()
    if confirm not in ['y', 'yes']:
        print("\n❌ Tax Payment Cancelled.\n")
        return
    
    if deduct_balance(acc, amount):
        add_transaction(acc, f"Tax Payment - Ref {tax_id}", amount, "tax")
        
        print("="*50)
        print("     🎉 TAX PAYMENT SUCCESSFUL!     ")
        print("="*50)
        print(f"   Reference: {tax_id}")
        print(f"   Amount   : Rs {amount:,.2f}")
        print("   Your tax has been paid successfully.\n")

def challan_payment(acc):
    print("\n" + "="*50)
    print("            CHALLAN PAYMENT             ")
    print("="*50)
    
    print("Pay Government Challan, Fees, Fines, etc.\n")
    
    while True:
        challan = input("Enter Challan Number: ").strip()
        if challan == "":
            print("❌ Challan number cannot be empty.\n")
            continue
        break
    
    while True:
        try:
            amount_input = input("Enter Challan Amount (Rs): ").strip()
            amount = float(amount_input)
            if amount <= 0:
                print("❌ Amount must be greater than zero.\n")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid numeric amount.\n")
    
    print(f"\nChallan Payment Summary:")
    print(f"   Challan No: {challan}")
    print(f"   Amount    : Rs {amount:,.2f}")
    
    confirm = input("\nProceed with Challan Payment? (y/n): ").lower()
    if confirm not in ['y', 'yes']:
        print("\n❌ Challan Payment Cancelled.\n")
        return
    
    if deduct_balance(acc, amount):
        add_transaction(acc, f"Challan Payment - {challan}", amount, "challan")
        
        print("="*50)
        print("     🎉 CHALLAN PAYMENT SUCCESSFUL!     ")
        print("="*50)
        print(f"   Challan No: {challan}")
        print(f"   Amount Paid: Rs {amount:,.2f}")
        print("   Payment completed successfully.\n")

    # ---------------- CHANGE PIN ----------------
def change_pin(acc):
    print("\n" + "="*50)
    print("              CHANGE PIN               ")
    print("="*50 + "\n")

    # Verify old PIN
    old_pin = input("Enter your current PIN: ").strip()
    if old_pin != acc["pin"]:
        print("❌ Incorrect current PIN.\n")
        return

    # New PIN input
    while True:
        new_pin = input("Enter new 4-digit PIN: ").strip()

        if not validate_pin(new_pin):
            print("❌ PIN must be exactly 4 digits.\n")
            continue

        weak_pins = ["0000", "1234", "1111", "2222", "9999", "9876", "5678"]
        if new_pin in weak_pins:
            print("⚠️  This PIN is weak. Choose a stronger one.\n")
            continue

        confirm_pin = input("Confirm new PIN: ").strip()
        if confirm_pin != new_pin:
            print("❌ PINs do not match.\n")
            continue

        break

    acc["pin"] = new_pin
    save_users()

    print("\n✅ PIN changed successfully!")
    print("Please use your new PIN next time you login.\n")
def admin_adjust_balance():
    print("\n" + "="*50)
    print("        ADMIN BALANCE CONTROL")
    print("="*50)

    cnic = input("Enter User CNIC: ").strip()

    if cnic not in USERS:
        print("❌ User not found.")
        return

    if cnic == "00000-0000000-0":
        print("❌ Cannot modify ADMIN account.")
        return

    user = USERS[cnic]

    print(f"\nUser Name : {user['name']}")
    print(f"Balance   : Rs {user['balance']:,.2f}\n")

    print("1. Add Money")
    print("2. Deduct Money")

    choice = input("Choose option: ").strip()

    try:
        amount = float(input("Enter Amount (Rs): ").strip())
        if amount <= 0:
            print("❌ Amount must be greater than zero.")
            return
    except ValueError:
        print("❌ Invalid amount.")
        return

    if choice == "1":
        user["balance"] += amount
        action = "Admin Credit"
        sign = "+"

    elif choice == "2":
        if user["balance"] < amount:
            print("❌ Insufficient balance to deduct.")
            return
        user["balance"] -= amount
        action = "Admin Deduction"
        sign = "-"

    else:
        print("❌ Invalid option.")
        return

    # Record transaction
    transaction = {
        "description": action,
        "date": datetime.now().strftime("%b %d, %Y"),
        "time": datetime.now().strftime("%I:%M %p"),
        "amount": f"{sign}{amount:,.2f}",
        "type": "admin",
        "balance_after": user["balance"]
    }

    user["transactions"].append(transaction)
    save_users()

    print("\n✅ Balance Updated Successfully!")
    print(f"New Balance: Rs {user['balance']:,.2f}\n")

# ---------------- START MENU ----------------

def start_menu():
    print("\n======== CASHIT SYSTEM ========")
    print("1. Login")
    print("2. Create New Account")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        return login()
    elif choice == "2":
        create_account()
        return start_menu()
    else:
        print("Goodbye!")
        exit()

# ---------------- MAIN ----------------

def main():
    while True:   
        acc = start_menu()

        if acc["cnic"] == "00000-0000000-0":
            admin_dashboard()
            continue   

        show_dashboard(acc)

        while True:
            print("Choose Payment Type:")
            print("1. Transfer")
            print("2. Bill Payment")
            print("3. Tax Payment")
            print("4. Challan Payment")
            print("5. View Dashboard Again")
            print("6. Change PIN")
            print("7. Logout")

            choice = input("Enter option: ")

            if choice == "1":
                transfer_payment(acc)
            elif choice == "2":
                bill_payment(acc)
            elif choice == "3":
                tax_payment(acc)
            elif choice == "4":
                challan_payment(acc)
            elif choice == "5":
                show_dashboard(acc)
            elif choice == "6":
                change_pin(acc)
            elif choice == "7":
                print("\nLogged Out. Returning to main menu...\n")
                break  
            else:
                print("Invalid Option.\n")


main()
