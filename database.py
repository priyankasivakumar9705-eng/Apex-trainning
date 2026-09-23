import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()
print("Connected Successfully")
while True:
    print("\n===== BANK MANAGEMENT SYSTEM =====")
    print("1. Create Account")
    print("2. Display Accounts")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Check Balance")
    print("6. Exit")

    choice = input("Enter your choice: ")

    # Create account
    if choice == "1":
        name = input("Enter customer name: ")
        balance = float(input("Enter initial balance: "))

        sql = "INSERT INTO account (customer_name, balance) VALUES (%s, %s)"
        values = (name, balance)

        cursor.execute(sql, values)
        conn.commit()

        print("Account created successfully!")
        print("Account number:", cursor.lastrowid)

    # Display accounts
    elif choice == "2":
        cursor.execute("SELECT * FROM account")
        records = cursor.fetchall()

        for row in records:
            print(row)

    # Deposit
    elif choice == "3":
        acc_no = int(input("Enter account number: "))
        amount = float(input("Enter deposit amount: "))

        sql = "UPDATE account SET balance = balance + %s WHERE account_no = %s"
        cursor.execute(sql, (amount, acc_no))
        conn.commit()

        print("Amount deposited successfully!")

    # Withdraw
    elif choice == "4":
        acc_no = int(input("Enter account number: "))
        amount = float(input("Enter withdrawal amount: "))

        sql = "UPDATE account SET balance = balance - %s WHERE account_no = %s"
        cursor.execute(sql, (amount, acc_no))
        conn.commit()

        print("Amount withdrawn successfully!")

    # Check balance
    elif choice == "5":
        acc_no = int(input("Enter account number: "))

        cursor.execute(
            "SELECT customer_name, balance FROM account WHERE account_no = %s",
            (acc_no,)
        )

        record = cursor.fetchone()

        if record:
            print("Customer:", record[0])
            print("Balance:", record[1])
        else:
            print("Account not found!")

    # Exit
    elif choice == "6":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")

cursor.close()
conn.close()