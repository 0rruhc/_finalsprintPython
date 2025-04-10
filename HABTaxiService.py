## Date: April 10, 2025
## Authors: Robot Group 1
## Description: Program to manage a taxi service company.

# import libraries
import datetime

# Constants 
CUR_DATE = datetime.datetime.now()
ALLOWED_CHARS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ .-'abcdefghijklmnopqrstuvwxyz0123456789")

# Open Defaults.dat file and read the contents
with open("Defaults.dat", "r") as f:
    nextTransactionNumber = int(f.readline())
    nextDriverNumber = int(f.readline())
    monthlyStandFee = float(f.readline())
    dailyRentalFee = float(f.readline())
    weeklyRentalFee = float(f.readline())
    hstRate = float(f.readline())
    lastStandFeeDate = f.readline().strip()

# Tables
employees = []
revenues = []
expenses = []
carRentals = []
payments = []

# Date handling
# Get today's date and the last stand fee date
today = datetime.date.today()
try:
    feeDate = datetime.datetime.strptime(lastStandFeeDate, "%Y-%m-%d").date()
except ValueError:
    feeDate = today  # Default to today if lastStandFeeDate is invalid


# Main Program
while True:
    print("\n")
    print(" " * 10 + "HAB Taxi Service")
    print(" " * 7 + "Company Service System")
    print("\n")
    print("1. Enter a New Employee (driver).")
    print("2. Enter Company Revenues.")
    print("3. Enter Company Expenses.")
    print("4. Track Car Rentals.")
    print("5. Record Employee Payment.")
    print("6. Print Company Profit Listing.")
    print("7. Print Driver Financial Listing.")
    print("8. Quit Program.")
    print("\n")
    
    # Get user input for choice number
    try:
        choice = int(input("Enter a Choice (1-8): "))
    except:
        print("Invalid input. Please enter a number between 1 and 8.")
        continue

    # Validate choice number
    if choice < 1 or choice > 8:
        print("Invalid choice. Please enter a number between 1 and 8.")
        continue
    
    # Input and validation for employee name
    if choice == 1:
        name = input("Enter Employee (Driver) name: ")
        if name and all(c in ALLOWED_CHARS for c in name):
            new_driver = {"id": nextDriverNumber, "name": name, "ownCar": True}  # Assuming ownCar = True for now
            employees.append(new_driver)
            nextDriverNumber += 1
            print(f"Driver {name} added.")
        else:
            print("Invalid name.")
    
    # Input and validation for revenue amount
    elif choice == 2:
        try:
            amount = float(input("Enter revenue amount: "))
            description = input("Enter revenue description: ")
            tax = round(amount * hstRate, 2)
            total = round(amount + tax, 2)
            revenues.append([nextTransactionNumber, CUR_DATE.date(), description, "company", amount, tax, total])
            nextTransactionNumber += 1
            print("Revenue recorded.")
        except:
            print("Invalid revenue amount.")

    # Input and validation for expense amount
    elif choice == 3:
        try:
            amount = float(input("Enter expense amount: "))
            description = input("Enter expense description: ")
            expenses.append([CUR_DATE.date(), description, amount])
            print("Expense recorded.")
        except:
            print("Invalid expense amount.")

    # Input and validation for car rental info
    elif choice == 4:
        rental = input("Enter car rental info: ")
        if rental and all(c in ALLOWED_CHARS for c in rental):
            carRentals.append(rental)
            print("Car rental recorded.")
        else:
            print("Invalid input.")

    # Input and validation for employee payment info
    elif choice == 5:
        payment = input("Enter employee payment info: ")
        if payment and all(c in ALLOWED_CHARS for c in payment):
            payments.append(payment)
            print("Payment recorded.")
        else:
            print("Invalid input.")

    # Print company profit listing
    elif choice == 6:
        totalRevenue = sum(r[6] for r in revenues)
        totalExpenses = sum(e[2] for e in expenses)
        print(f"Total Profit: {round(totalRevenue - totalExpenses, 2)}")

    # Print driver financial listing
    elif choice == 7:
        for emp in employees:
            print(f"Driver ID: {emp['id']}, Name: {emp['name']}")

    # Quit program
    elif choice == 8:
        print("Exiting program.")
        break
    
    # Monthly stand fees
    # Check if today is the first of the month and if the fee has already been applied
    feeApplied = False
    if today.day == 1 and today > feeDate:
        for driver in employees:
            if driver.get("ownCar", False):
                amount = monthlyStandFee
                tax = round(amount * hstRate, 2)
                total = round(amount + tax, 2)

                # Add the fee to revenues
                revenues.append([
                    nextTransactionNumber,
                    today.strftime("%Y-%m-%d"),
                    "Monthly Stand Fees",
                    driver["id"],
                    round(amount, 2),
                    tax,
                    total
                ])

                # Update the driver record with the new fee
                driver["standFee"] = round(amount, 2)
                nextTransactionNumber += 1
                feeApplied = True

    # Update lastStandFeeDate to today
    if feeApplied:
        lastStandFeeDate = today.strftime("%Y-%m-%d")

# Save to Defaults.dat
f = open("Defaults.dat", "w")
with open("Defaults.dat", "w") as f:
    f.write(str(nextTransactionNumber) + "\n")
    f.write(str(nextDriverNumber) + "\n")
    f.write(str(monthlyStandFee) + "\n")
    f.write(str(dailyRentalFee) + "\n")
    f.write(str(weeklyRentalFee) + "\n")
    f.write(str(hstRate) + "\n")
    f.write(lastStandFeeDate + "\n")
