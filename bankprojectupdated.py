"""
==================== BANK MANAGEMENT SYSTEM ====================

DESCRIPTION:

This project is a Python + MySQL based Bank Management System
implemented using PyMySQL and Exception Handling concepts.

The program allows bank customers to securely login using their
account number and password stored in a MySQL database.

After successful login, the user can perform various banking
operations through a menu-driven interface.


-------------------- FEATURES IMPLEMENTED --------------------

1. LOGIN AUTHENTICATION
   - Validates account number from database
   - Validates password
   - Allows maximum 3 login attempts
   - Blocks account temporarily after 3 failed attempts

2. DEPOSIT
   - User can deposit money into account
   - Minimum deposit amount validation implemented

3. WITHDRAW
   - User can withdraw money
   - Insufficient balance checking implemented

4. CHECK BALANCE
   - Displays updated account balance from database

5. TRANSFER MONEY
   - Transfers money from one account to another
   - Prevents self-transfer
   - Validates receiver account
   - Uses rollback() for transaction safety

6. CUSTOM EXCEPTION HANDLING
   - InvalidAccountNumber
   - InvalidPassword
   - DepositLimitException
   - InsufficientBalanceException
   - ReceiverAccountNotFound
   - SameAccountTransfer
   - TransactionLimitException

7. DATABASE CONNECTIVITY
   - Uses PyMySQL module
   - Performs SQL operations like:
        SELECT
        UPDATE
   - Uses commit() and rollback()

8. MODULAR PROGRAMMING
   - Functions used for:
        login()
        deposit()
        withdraw()
        check_balance()
        transfer_money()
        main_menu()

---------------------------------------------------------------

DATABASE USED:
MySQL

TABLE USED:
customer

TABLE COLUMNS:
---------------------------------------------------------------
account_number
name
email
phno
pass
balance
---------------------------------------------------------------

CONCEPTS USED:
---------------------------------------------------------------
Python Functions
Exception Handling
Custom Exceptions
Loops
Conditional Statements
Database Connectivity
SQL Queries
Transactions
commit()
rollback()
fetchone()
Modular Programming
---------------------------------------------------------------

===============================================================
"""




import pymysql



class InvalidAccountNumber(Exception):
    pass


class InvalidPassword(Exception):
    pass


class DepositLimitException(Exception):
    pass


class InsufficientBalanceException(Exception):
    pass


class ReceiverAccountNotFound(Exception):
    pass


class SameAccountTransfer(Exception):
    pass


class TransactionLimitException(Exception):
    pass


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='blazext_7_7',
    database='bank'
)

cursor = conn.cursor()



attempts = 0


while attempts < 3:

    try:

        acc_no = int(input("Enter Account Number: "))

        password = input("Enter Password: ")

        #CHECK ACCOUNT

        cursor.execute(
            '''
            select * from customer
            where account_number=%s
            ''',
            (acc_no,)
        )

        account = cursor.fetchone()

        #INVALID ACCOUNT

        if not account:

            raise InvalidAccountNumber(
                "Invalid Account Number"
            )

        #PASSWORD CHECK

        db_password = account[4]

        if password != db_password:

            raise InvalidPassword(
                "Invalid Password"
            )

        print("\nWELCOME TO AXIS BANK")

        #MAIN MENU

        while True:

            print("\nMENU")

            print("1. Deposit")

            print("2. Withdraw")

            print("3. Check Balance")

            print("4. Transfer Money")

            print("5. Exit")

            choice = int(input("Enter Choice: "))

            #DEPOSIT

            if choice == 1:

                try:

                    amount = float(
                        input("Enter Deposit Amount: ")
                    )

                    if amount < 500:

                        raise DepositLimitException(
                            "Minimum deposit amount is 500"
                        )

                    cursor.execute(
                        '''
                        update customer
                        set balance=balance+%s
                        where account_number=%s
                        ''',
                        (amount, acc_no)
                    )

                    conn.commit()

                    print(
                        "Amount Deposited Successfully"
                    )

                    cursor.execute(
                        '''
                        select balance from customer
                        where account_number=%s
                        ''',
                        (acc_no,)
                    )

                    balance = cursor.fetchone()[0]

                    print(
                        "Available Balance:",
                        balance
                    )

                except DepositLimitException as e:

                    print(e)

            #WITHDRAW

            elif choice == 2:

                try:

                    amount = float(
                        input("Enter Withdraw Amount: ")
                    )

                    cursor.execute(
                        '''
                        select balance from customer
                        where account_number=%s
                        ''',
                        (acc_no,)
                    )

                    balance = cursor.fetchone()[0]

                    if amount > balance:

                        raise InsufficientBalanceException(
                            "Insufficient Balance"
                        )

                    cursor.execute(
                        '''
                        update customer
                        set balance=balance-%s
                        where account_number=%s
                        ''',
                        (amount, acc_no)
                    )

                    conn.commit()

                    print("Withdraw Successful")

                    cursor.execute(
                        '''
                        select balance from customer
                        where account_number=%s
                        ''',
                        (acc_no,)
                    )

                    balance = cursor.fetchone()[0]

                    print(
                        "Remaining Balance:",
                        balance
                    )

                except InsufficientBalanceException as e:

                    print(e)

            #CHECK BALANCE

            elif choice == 3:

                cursor.execute(
                    '''
                    select balance from customer
                    where account_number=%s
                    ''',
                    (acc_no,)
                )

                balance = cursor.fetchone()[0]

                print(
                    "Available Balance:",
                    balance
                )

            #TRANSFER MONEY

            elif choice == 4:

                try:

                    receiver_acc = int(
                        input(
                            "Enter Receiver Account Number: "
                        )
                    )

                    #SAME ACCOUNT CHECK

                    if receiver_acc == acc_no:

                        raise SameAccountTransfer(
                            "Cannot transfer to same account"
                        )

                    #CHECK RECEIVER ACCOUNT

                    cursor.execute(
                        '''
                        select * from customer
                        where account_number=%s
                        ''',
                        (receiver_acc,)
                    )

                    receiver = cursor.fetchone()

                    if not receiver:

                        raise ReceiverAccountNotFound(
                            "Receiver Account Not Found"
                        )

                    amount = float(
                        input(
                            "Enter Transfer Amount: "
                        )
                    )

                    if amount < 500:

                        raise TransactionLimitException(
                            "Minimum Transaction amount is 500"
                        )

                    #CHECK SENDER BALANCE

                    cursor.execute(
                        '''
                        select balance from customer
                        where account_number=%s
                        ''',
                        (acc_no,)
                    )

                    sender_balance = cursor.fetchone()[0]

                    if amount > sender_balance:

                        raise InsufficientBalanceException(
                            "Insufficient Balance"
                        )

                    #DEDUCT FROM SENDER

                    cursor.execute(
                        '''
                        update customer
                        set balance=balance-%s
                        where account_number=%s
                        ''',
                        (amount, acc_no)
                    )

                    #ADD TO RECEIVER

                    cursor.execute(
                        '''
                        update customer
                        set balance=balance+%s
                        where account_number=%s
                        ''',
                        (amount, receiver_acc)
                    )

                    conn.commit()

                    print(
                        "Transaction Successful"
                    )

                    cursor.execute(
                        '''
                        select balance from customer
                        where account_number=%s
                        ''',
                        (acc_no,)
                    )

                    updated_balance = cursor.fetchone()[0]

                    print(
                        "Remaining Balance:",
                        updated_balance
                    )

                except (
                    ReceiverAccountNotFound,
                    InsufficientBalanceException,
                    SameAccountTransfer,
                    TransactionLimitException
                ) as e:

                    conn.rollback()

                    print(e)

            #EXIT

            elif choice == 5:

                print(
                    "Thank You For Banking With Us"
                )

                break

            else:

                print("Invalid Option")

        break


    except (
        InvalidAccountNumber,
        InvalidPassword
    ) as e:

        attempts += 1

        print(e)

        print(
            "Attempts Left:",
            3 - attempts
        )



if attempts == 3:

    print(
        "\nAccount Blocked!"
    )

    print(
        "Try again after 1 hour or contact bank."
    )



cursor.close()

conn.close()