
import streamlit as st
import pymysql
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# MySQL Connection
conn = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = conn.cursor()

# Login status
if "login" not in st.session_state:
    st.session_state.login = False

if "login_type" not in st.session_state:
    st.session_state.login_type = ""

# ---------------- LOGIN ----------------

if not st.session_state.login:

    st.title("🔐 Bank Login")

    login_type = st.selectbox(
        "Select Login Type",
        ["Customer Login", "Admin Login"]
    )

    if login_type == "Customer Login":

        username = st.text_input("Customer Username")
        pin = st.text_input("Customer PIN", type="password")

        if st.button("Customer Login"):

            if username == "priya" and pin == "1234":
                st.session_state.login = True
                st.session_state.login_type = "Customer"
                st.success("Customer Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or PIN")

    else:

        username = st.text_input("Admin Username")
        password = st.text_input("Admin Password", type="password")

        if st.button("Admin Login"):

            if username == "admin" and password == "admin123":
                st.session_state.login = True
                st.session_state.login_type = "Admin"
                st.success("Admin Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")


# ---------------- BANK SYSTEM ----------------

else:

    st.title("🏦 Bank Management System")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.login_type = ""
        st.rerun()

    # -------- ADMIN --------

    if st.session_state.login_type == "Admin":

        st.sidebar.success("👨‍💼 Admin")

        menu = st.sidebar.selectbox(
            "Select Option",
            ["Create Account", "Delete ID", "Check All Values"]
        )

        # Create Account
        if menu == "Create Account":

            st.header("Create Account")

            name = st.text_input("Customer Name")
            balance = st.number_input(
                "Initial Balance",
                min_value=0.0
            )

            if st.button("Create Account"):

                cursor.execute(
                    """
                    INSERT INTO account
                    (customer_name, balance)
                    VALUES (%s, %s)
                    """,
                    (name, balance)
                )

                conn.commit()

                st.success("Account Created Successfully!")

        # Delete Account
        elif menu == "Delete ID":

            st.header("Delete Account")

            acc_no = st.number_input(
                "Account Number",
                min_value=1
            )

            if st.button("Delete Account"):

                cursor.execute(
                    "DELETE FROM account WHERE account_no=%s",
                    (acc_no,)
                )

                conn.commit()

                if cursor.rowcount > 0:
                    st.success("Account Deleted!")
                else:
                    st.error("Account Not Found!")

        # Check All Values
        elif menu == "Check All Values":

            st.header("All Customer Details")

            cursor.execute("SELECT * FROM account")

            records = cursor.fetchall()

            st.dataframe(records)

    # -------- CUSTOMER --------

    else:

        st.sidebar.success("👤 Customer")

        menu = st.sidebar.selectbox(
            "Select Option",
            ["Deposit", "Withdraw", "Check Balance"]
        )

        # Deposit
        if menu == "Deposit":

            st.header("💰 Deposit")

            acc_no = st.number_input(
                "Account Number",
                min_value=1
            )

            amount = st.number_input(
                "Deposit Amount",
                min_value=0.0
            )

            if st.button("Deposit"):

                cursor.execute(
                    """
                    UPDATE account
                    SET balance = balance + %s
                    WHERE account_no = %s
                    """,
                    (amount, acc_no)
                )

                conn.commit()

                if cursor.rowcount > 0:
                    st.success("Amount Deposited!")
                else:
                    st.error("Account Not Found!")

        # Withdraw
        elif menu == "Withdraw":

            st.header("💸 Withdraw")

            acc_no = st.number_input(
                "Account Number",
                min_value=1
            )

            amount = st.number_input(
                "Withdrawal Amount",
                min_value=0.0
            )

            if st.button("Withdraw"):

                cursor.execute(
                    """
                    SELECT balance
                    FROM account
                    WHERE account_no=%s
                    """,
                    (acc_no,)
                )

                record = cursor.fetchone()

                if record:

                    balance = float(record[0])

                    if amount <= balance:

                        cursor.execute(
                            """
                            UPDATE account
                            SET balance = balance - %s
                            WHERE account_no=%s
                            """,
                            (amount, acc_no)
                        )

                        conn.commit()

                        st.success("Amount Withdrawn!")

                    else:
                        st.error("Insufficient Balance!")

                else:
                    st.error("Account Not Found!")

        # Check Balance
        elif menu == "Check Balance":

            st.header("💰 Check Balance")

            acc_no = st.number_input(
                "Account Number",
                min_value=1
            )

            if st.button("Check Balance"):

                cursor.execute(
                    """
                    SELECT customer_name, balance
                    FROM account
                    WHERE account_no=%s
                    """,
                    (acc_no,)
                )

                record = cursor.fetchone()

                if record:

                    st.write("Customer Name:", record[0])
                    st.write("Balance: ₹", record[1])

                else:
                    st.error("Account Not Found!")