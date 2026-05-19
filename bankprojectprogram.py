class InvalidAccountNumber(Exception):
    pass
class InvalidPassword(Exception):
    pass
class DepositLimitException(Exception):
    pass
class InsufficientBalanceException(Exception):
    pass
correct_account_number="1234"
correct_password="admin1234"
balance=100000
attempts=0
while attempts<3:
    try:
        acc_no=input("enter account number: ")
        password=input("enter password: ")
        if acc_no!=correct_account_number:
            raise InvalidAccountNumber("invalid account number")
        if password != correct_password:
            raise InvalidPassword("invalid password")
        print("\nWelcome to Axis Bank")
        while True:
            print("\nChoose any one option")
            print("1.deposit")
            print("2.withdraw")
            print("3.balance")
            print("4.exit")
            choice=int(input("Enter Choice "))
            if choice==1:
                try:
                    amount=float(input("Enter Deposit Amount: "))
                    if amount<500:
                        raise DepositLimitException("minimum deposit amount is 500")
                    balance+=amount
                    print("Amount Deposited Successfully")
                    print("Available Balance:", balance)
                except DepositLimitException as e:
                    print(e)
            elif choice==2:
                try:
                    amount=float(input("Enter Withdraw Amount: "))
                    if amount>balance:
                        raise InsufficientBalanceException("insufficient balance")
                    balance-=amount
                    print("Withdraw Successful")
                    print("Remaining Balance:",balance)
                except InsufficientBalanceException as e:
                    print(e)
            elif choice==3:
                print("available balance:",balance)
            elif choice==4:
                print("Thank You")
                break
            else:
                print("Invalid Option")
        break
    except (InvalidAccountNumber,InvalidPassword) as e:
        attempts+=1
        print(e)
        print("attempts Left:",3-attempts)
if attempts==3:
    print("Account blocked!Try logging after 1 hour or try reaching your bank:)")