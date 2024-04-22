import random
import mysql.connector
from tabulate import tabulate
import re
from datetime import datetime

class Bank:
    def __init__(self):
        self.mydb = mysql.connector.connect(
        host="localhost", user="root", password="oneteam", database="akshith")
        self.mycursor = self.mydb.cursor()
        self.log = None

    def acc_no(self):
        acc_no = ""
        for _ in range(6):
            random_digit = random.randint(0, 9)
            acc_no += str(random_digit)
        return acc_no

    def login(self):
        usr_nme = input("Enter Your Username: ")
        pswd = input("Enter Your Password: ")
        self.mycursor.execute(
            "SELECT usr, fl_name,accno FROM customer WHERE usr = %s AND pswd = %s",
            (usr_nme, pswd),
        )
        user = self.mycursor.fetchone()

        if user:
            usr_nme, fl_name, accno = user
            print(" ")
            print(f"*******Login successfull Welcome {fl_name} **********")
            print(" ")
            self.log = {"usr_nme": usr_nme, "accno": accno}
        else:
            print("")
            print("***********Invalid username or password*************")
            print("")
            print(self.selector())

    def staff(self):
        usr_nme = input("Enter Your Username: ")
        pswd = input("Enter Your Password: ")
        self.mycursor.execute(
            "SELECT usr_nme FROM staff WHERE usr_nme = %s AND pswd = %s",
            (usr_nme, pswd),
        )
        user = self.mycursor.fetchone()

        if user:
            usr_nme = user
            print(" ")
            print(" ")
            print("-" * 50)
            self.log = {"usr_nme": usr_nme}
        else:
            print(" ")
            print("-----------Invalid username or password-----------")
            print(" ")
            print(self.selector())


    def new_account(self):
        name = input("Enter Your name: ")
        acty = input("Enter Your Account Type - Saving/Current (S/C): ")
        while True:
            emi = input("Enter your email address : ")
            # Regular expression pattern for validating email addresses
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, emi):
                print("Invalid email address. Please enter a valid email address.")
            else:
                break  # Break out of the loop if the email is valid
        while True:
            dob_input = input("Enter Your Date Of Birth (YYYY-MM-DD): ")
            try:
                dob = datetime.strptime(dob_input, '%Y-%m-%d')
                if dob.year > 2023:
                    print("Invalid date of birth. Please enter a date before 2024.")
                else:
                    break 
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                
        address = input("Enter Your Address: ")
        while True:
            contact = input("Enter Your Phone Number: ")
            if len(contact) > 10:
                print("Invalid contact number. Please enter a 10-digit number.")
            else:
                break  # Break out of the loop if the contact number is valid
        gender = input("Enter Your Gender- Male/Female (M/F): ")
        ac_no = self.acc_no()
        usr = input("Enter Your Username: ")
        while True:
            psw = input("Enter Your Password: ")
            if len(psw) < 8:
                print("Password must be at least 8 characters long.")
            else:
                break
        amount = int(input("Enter the Initial amount (>=500):"))
        if amount < 500:
            print("Minimum amount required is 500.")
        else:
            sq = (name, acty, emi, dob_input, address, contact, gender, ac_no, usr, psw, amount,)
            sq2 = (ac_no,)
            qy = "INSERT INTO customer (fl_name, ac_type, emi, dob, adr, cnt, gen, accno, usr, pswd, bal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            qy1 = "INSERT INTO transaction (accno, trans_type, amount) VALUES (%s, 'Deposit', %s)"
            sq2 = (ac_no, amount)
            self.mycursor.execute(qy, sq)
            self.mycursor.execute(qy1, sq2)
            self.mydb.commit()
            print("New Account Number is", ac_no)


    def deposit(self):
        if self.log:
            amount = float(input("Enter Your Amount: "))
            ac = self.log["accno"]
            a = "SELECT bal FROM customer WHERE accno = %s"
            info = (ac,)
            self.mycursor.execute(a, info)
            result = self.mycursor.fetchone()
            cur = result[0] + amount
            qy = "UPDATE customer SET bal = %s WHERE accno = %s"
            sq1 = (cur, ac)
            self.mycursor.execute(qy, sq1)
            # Deposit
            qy1 = "INSERT INTO transaction (accno, trans_type,amount) VALUES (%s, 'Deposit', %s)"
            sq2 = (ac, amount)
            self.mycursor.execute(qy1, sq2)
            self.mydb.commit()
            print("")
            print("***************Deposited**************")
            print("")
            print("New Balance:", cur)
        else:
            print("Please log in first.")

    def check_balance(self):
        if self.log:
            ac = self.log["accno"]
            a = "SELECT bal FROM customer WHERE accno = %s"
            info = (ac,)
            self.mycursor.execute(a, info)
            result = self.mycursor.fetchone()
            print("Your Account balance is:", result[-1])
        else:
            print("Please log in first.")

    def withdraw(self):
        if self.log:
            amount = float(input("Enter Your Amount: "))
            ac = self.log["accno"]
            ab = "SELECT bal FROM customer WHERE accno = %s"
            inf = (ac,)
            self.mycursor.execute(ab, inf)
            res = self.mycursor.fetchone()
            current_balance = res[0]

            if amount > current_balance:
                print("-" * 50)
                print("Insufficient Balance...".center(50))
            else:
                z = current_balance - amount
                qy = "UPDATE customer SET bal = %s WHERE accno = %s"
                inf = (z, ac)
                self.mycursor.execute(qy, inf)
                qy1 = "INSERT INTO transaction (accno, trans_type,amount) VALUES (%s, 'Withdrawal', %s)"
                inf1 = (ac, -amount)
                self.mycursor.execute(qy1, inf1)
                self.mydb.commit()
                print("")
                print("***************Withdrawal Completed***************")
                print("")
                print("New Balance:", z)
        else:
            print("Please log in first.")

    from tabulate import tabulate

    def user_details(self):
        if self.log:
            ac = self.log["accno"]
            qy = "SELECT fl_name, dob, ac_type, bal, adr, cnt, gen, accno, usr, emi FROM customer WHERE accno = %s"
            self.mycursor.execute(qy, (ac,))
            res = self.mycursor.fetchone()
            if res:
                print("Customer's Details")
                headers = [
                    "Name",
                    "Date of Birth",
                    "Account Type",
                    "Balance",
                    "Address",
                    "Contact No",
                    "Gender",
                    "Account No",
                    "Username",
                    "Email"
                ]
                try:
                    data = [
                        [res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9]]
                    ]
                except IndexError:
                    print("Not enough elements in 'res' tuple.")
                    return
                print(tabulate(data, headers=headers, tablefmt="grid"))
            else:
                print("No customer found!")
        else:
            print("Please log in first.")


    def user_transaction(self):  # user view transaction
        if self.log:
            ac = self.log["accno"]
            qy = "SELECT * FROM transaction WHERE accno=%s ORDER BY date_time DESC"
            info = (ac,)
            self.mycursor.execute(qy, info)
            result = self.mycursor.fetchall()
            if result:
                print("Transaction History")
                headers = [
                    "Transaction Id",
                    "Account No",
                    "Transaction Type",
                    "Amount",
                    "Date/Time",
                ]
                data = [
                    [user[0], user[1], user[2], user[3], user[4]] for user in result
                ]
                print(tabulate(data, headers=headers, tablefmt="grid"))
            else:
                print("No Transaction History.")
        else:
            print("Please log in first.")

    def transaction_view(self):  # staff view Transaction
        qy = "SELECT * FROM transaction ORDER BY date_time DESC"
        self.mycursor.execute(qy)
        result = self.mycursor.fetchall()
        if result:
            print("Transaction History")
            headers = [
                "Transaction Id",
                "Account No",
                "Transaction Type",
                "Amount",
                "Date/Time",
            ]
            data = [[user[0], user[1], user[2], user[3], user[4]] for user in result]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print("No Transaction History.")

    def close_account(self):
        ac = int(input("Enter the account number : "))
        dlt = "delete from customer where accno=%s"
        self.mycursor.execute(dlt, (ac,))
        self.mydb.commit()
        print("")
        print("*************Account closed *****************")
        print("")


    def staff_update(self):
        ac = int(input("Enter the Account no :"))
        qy = "SELECT accno, emi FROM customer WHERE accno=%s"
        info = (ac,)
        self.mycursor.execute(qy, info)
        user = self.mycursor.fetchone()

        if user:
            print("*" * 50)
            print("1. Update Name")
            print("2. Update Email Address")
            print("3. Update Phone Number")
            print("4. Update Address")
            print("5. Update Password")
            print("6. Menu")
            print("*" * 50)
            option = input("Enter your option (1/2/3/4/5/6): ")

            if option == "1":
                name = input("Enter your First name: ")
                qy = "UPDATE customer SET fl_name = %s WHERE accno=%s"
                inf = (name, ac)
                self.mycursor.execute(qy, inf)
                self.mydb.commit()
                print("")
                print("**********Name Updated**********")
                print("")
                
            elif option == "2":
                while True:
                    emi = input("Enter your new email address: ")
                    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', emi):
                        print("Invalid email address. Please enter a valid email address.")
                    else:
                        break  # Break out of the loop if the email is valid
                qy = "UPDATE customer SET emi = %s WHERE accno = %s"
                inf = (emi, ac)
                self.mycursor.execute(qy, inf)
                self.mydb.commit()
                print("")
                print("*******Email Address Updated*******")
                print("")
            elif option == "3":
                while True:
                    mob = input("Enter your new phone number: ")
                    if len(mob) != 10 or not mob.isdigit():
                        print("Invalid phone number. Please enter a 10-digit number.")
                    else:
                        break  # Break out of the loop if the phone number is valid
                qy = "UPDATE customer SET cnt = %s WHERE accno = %s"
                inf = (mob, ac)
                self.mycursor.execute(qy, inf)
                self.mydb.commit()
                print("")
                print("*******Phone Number Updated*******")
                print("")
            elif option == "4":
                ad = input("Enter your new address: ")
                qy = "UPDATE customer SET adr = %s WHERE accno = %s"
                inf = (ad, ac)
                self.mycursor.execute(qy, inf)
                self.mydb.commit()
                print("")
                print("*********Address Updated**********")
                print("")
            elif option == "5":
                while True:
                    psw = input("Enter your new password: ")
                    if len(psw) < 8:
                        print("Password must be at least 8 characters long.")
                    else:
                        break  # Break out of the loop if the password meets the minimum length requirement
                qy = "UPDATE customer SET pswd = %s WHERE accno = %s"
                inf = (psw, ac)
                self.mycursor.execute(qy, inf)
                self.mydb.commit()
                print("")
                print("*********Password Updated*********")
                print("")
            elif option == "6":
                pass
            else:
                print("Invalid option. Enter Again...")

        else:
            print("Account not Found!")


    def staff_view_details(self):
        qy = "SELECT * FROM customer"
        self.mycursor.execute(qy)
        cus = self.mycursor.fetchall()
        if cus:
            print("Customer's Details")
            headers = [
                "Name",
                "Date of Birth",
                "Account Type",
                "Balance",
                "Address",
                "Contact No",
                "gender",
                "Account No",
                "Username",
                "Password",
            ]
            data = [
                [res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9]]
                for res in cus
            ]
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print("No customer found!")


    def selector(self):
        print(" ")
        print(" ")
        print("1. Customer Login")
        print("2. staff Login")
        print(" ")
        option = input("Enter your Option (1/2): ")

        if option == "1":
            self.login()
            if self.log:
                while True:
                    print("")
                    print("")
                    print("*" * 18 + " Welcome ".center(16, "*") + "*" * 18)
                    print("")
                    print("1. Deposit amount")
                    print("2. Withdrawal amount")
                    print("3. Balance ")
                    print("4. Transaction History")
                    print("5. User details")
                    print("6. Exit")
                    print("*" * 51)
                    option = input("Enter your Option : ")

                    if option == "1":
                        self.deposit()
                    elif option == "2":
                        self.withdraw()
                    elif option == "3":
                        self.check_balance()
                    elif option == "4":
                        self.user_transaction()
                    elif option == "5":
                        self.user_details()
                    elif option == "6":
                        print("")
                        print(self.selector())
                    else:
                        print("Enter the correct Option (1/2/3/4/5): ")
            else:
                print("Invalid option. Please Enter Again.")

        elif option == "2":
            self.staff()
            if self.log:
                while True:
                    print("")
                    print("")
                    print("1. Customer details")
                    print("2. Update  details")
                    print("3. Transaction History")
                    print("4. Create New account")
                    print("5. Close account")
                    print("6. Exit")
                    print("--------------------------------------------s")
                    staff_option = input("Enter your option : ")

                    if staff_option == "1":
                        self.staff_view_details()
                    elif staff_option == "2":
                        self.staff_update()
                    elif staff_option == "3":
                        self.transaction_view()
                    elif staff_option == "4":
                        self.new_account()
                    elif staff_option == "5":
                        self.close_account()
                    elif staff_option == "6":
                        print("")
                        print(self.selector())
                    else:
                        print("Invalid Option. Please Enter Again.")
            else:
                print("Please Login First.")
        else:
            print("Please enter a correct option (1/2): ")

# Create an instance of the Bank class and call the selector method to start the program
bank = Bank()
bank.selector()