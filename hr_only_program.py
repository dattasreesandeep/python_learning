"""
=========================================================
EMPLOYEE MANAGEMENT SYSTEM USING PYMYSQL
=========================================================

PROJECT DESCRIPTION

This project is a role-based Employee Management System
developed using Python and MySQL (PyMySQL).

The system authenticates employees using Employee ID and
Password stored in the MySQL database and provides access
based on their designation.

---------------------------------------------------------
DATABASE TABLES
---------------------------------------------------------

1. roles
   Stores valid designations available in the company.

   Example:
   H - Human Resources
   P - Project Manager
   T - Team Lead
   S - Software Developer

2. employee_details
   Stores employee information such as:
   - Name
   - Age
   - Salary
   - Designation
   - Email IDs
   - Phone Number
   - Employee ID
   - Username
   - Password
   - Date of Birth
   - Joining Date

---------------------------------------------------------
FEATURES IMPLEMENTED
---------------------------------------------------------

1. Employee Login Authentication
   - Validates Employee ID
   - Validates Password
   - Allows maximum 3 login attempts
   - Blocks login after repeated failures

2. Role-Based Access Control
   - Human Resources employees receive admin access
   - Other employees receive read-only access

3. Employee Registration
   - HR can add new employees
   - Duplicate Employee IDs are prevented
   - Designation is validated against the roles table

4. Automatic Corporate Email Generation
   Format:
       First letter of Last Name +
       Full First Name +
       @miraclesoft.com

   Example:
       John Pork
       -> pjohn@miraclesoft.com

5. Automatic Password Generation
   Format:
       First 2 letters of First Name +
       Last 2 letters of Last Name +
       Special Character +
       Current Date and Time

   Example:
       John Pork @
       -> Jhok@202605281745

6. Employee Details Viewing
   - Displays all employee records stored in database

---------------------------------------------------------
CUSTOM EXCEPTIONS USED
---------------------------------------------------------

- InvalidEmployeeID
- InvalidPassword
- DuplicateEmployeeID
- InvalidDesignation
- UnauthorizedAccessException

---------------------------------------------------------
FUNCTIONS USED
---------------------------------------------------------

employee_exists()
generate_password()
login()
add_employee()
view_employees()
hr_menu()
employee_menu()

---------------------------------------------------------
TECHNOLOGIES USED
---------------------------------------------------------

- Python
- PyMySQL
- MySQL
- Exception Handling
- Functions
- Role-Based Authorization
- Database Connectivity

=========================================================
"""




import pymysql

from datetime import datetime



class InvalidEmployeeID(Exception):
    pass
class InvalidPassword(Exception):
    pass
class UnauthorizedAccessException(Exception):
    pass
class DuplicateEmployeeID(Exception):
    pass
class InvalidDesignation(Exception):
    pass

#DATABASE CONNECTION

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='blazext_7_7',
    database='company'
)

cursor = conn.cursor()

def employee_exists(emp_id):
    cursor.execute(
        '''
        select * from employee_details
        where Employee_ID=%s
        ''',(emp_id,)
    )
    return cursor.fetchone()


def generate_password(fname, lname, special_char):
    current_datetime = datetime.now().strftime("%Y%m%d%H%M")
    password = (fname[:2] +lname[-2:] +special_char + current_datetime)
    return password

#LOGIN FUNCTION

def login():
    attempts = 0

    while attempts < 3:

        try:

            emp_id = int(input("Enter Employee ID: "))
            password = input("Enter Employee Password: ")
            employee = employee_exists(emp_id)

            if not employee:
                raise InvalidEmployeeID("Invalid Employee ID")
            db_password = employee[10]

            if password != db_password:
                raise InvalidPassword("Invalid Password")
            
            print("\nLogin Successful")
            return employee
        
        except (InvalidEmployeeID,InvalidPassword) as e:
            attempts += 1
            print(e)
            print("Attempts Left:",3 - attempts)

    print("\nTry again after 5 mins")

    return None

#ADD EMPLOYEE FUNCTION

def add_employee():

    try:
        fname = input("Enter First Name: ")
        lname = input("Enter Last Name: ")
        age = int(input("Enter Age: "))
        salary = int(input("Enter Salary: "))
        designation = input("Enter Designation: ")
        personal_mail = input("Enter Personal Mail: ")
        corporate_mail = (lname[0].lower()+fname.lower() +"@miraclesoft.com")
        phone = int(input("Enter Phone Number: "))
        emp_id = int(input("Enter Employee ID: "))
        username = input("Enter Username: ")
        dob = input("Enter DOB (YYYY-MM-DD): ")
        joining_date = datetime.now()
        special_char = input("Enter Special Character: ")
        #CHECK DUPLICATE EMPLOYEE ID

        existing_employee = employee_exists(emp_id)

        if existing_employee:

            raise DuplicateEmployeeID(
                "Employee ID Already Exists"
            )

        #DESIGNATION VALIDATION

        cursor.execute(
            '''
            select * from roles
            where role=%s
            ''',
            (designation,)
        )

        role = cursor.fetchone()

        if not role:

            raise InvalidDesignation(
                "Invalid Designation"
            )

        #PASSWORD GENERATION

        password = generate_password(fname,lname,special_char)

        #INSERT QUERY

        cursor.execute(
            '''
            insert into employee_details
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',
            (
                fname,
                lname,
                age,
                salary,
                designation,
                personal_mail,
                corporate_mail,
                phone,
                emp_id,
                username,
                password,
                dob,
                joining_date
            )
        )

        conn.commit()

        print("\nEmployee Added Successfully")

        print("Generated Password:",password)

    except (DuplicateEmployeeID,InvalidDesignation) as e:
        
        print(e)


#VIEW EMPLOYEES FUNCTION

def view_employees():

    cursor.execute(
        '''
        select * from employee_details
        '''
    )

    employees = cursor.fetchall()

    print("\nEMPLOYEE DETAILS\n")

    for employee in employees:
        print(employee)
        print()


#HR MENU

def hr_menu():

    while True:

        print("\nHR MENU")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Exit")

        choice = int(input("Enter Choice: "))

        if choice == 1:
            add_employee()

        elif choice == 2:
            view_employees()

        elif choice == 3:
            print("Exiting HR Menu")

            break

        else:

            print("Invalid Choice")


#EMPLOYEE MENU

def employee_menu():

    while True:

        print("\nEMPLOYEE MENU")
        print("1. View Employees")
        print("2. Exit")
        choice = int(input("Enter Choice: "))

        if choice == 1:
            view_employees()

        elif choice == 2:
            print("Exiting Employee Menu")

            break

        else:

            print("Invalid Choice")


employee = login()

if employee:
    designation = employee[4]

    if designation == "Human Resources":
        hr_menu()

    else:

        employee_menu()

cursor.close()

conn.close()