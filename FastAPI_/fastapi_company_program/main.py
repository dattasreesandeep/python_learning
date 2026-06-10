from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from datetime import date, datetime

from database import engine, sessionlocal, metadata
from models import roles, employee

app = FastAPI()

metadata.create_all(bind=engine)


# DATABASE DEPENDENCY

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


# PYDANTIC MODELS

class Login(BaseModel):
    username: str
    password: str
    designation: str


class EmployeeCreate(BaseModel):

    first_name: str
    last_name: str

    age: int
    salary: float

    designation: str

    personal_mail: str
    phone: int

    dob: date
    doj: date

class EmployeeAddRequest(EmployeeCreate):

    login_username: str
    login_password: str


# INSERT ROLES

@app.post("/roles")
def insert_roles(db: Session = Depends(get_db)):

    data = [
        ("H", "HumanResourceManager"),
        ("P", "ProjectManager"),
        ("T", "TeamLead"),
        ("S", "SoftwareDeveloper")
    ]

    for role in data:
        try:

            stmt = insert(roles).values(
                RoleId=role[0],
                RoleName=role[1]
            )

            db.execute(stmt)

        except:
            pass

    db.commit()

    return {
        "msg": "Roles Inserted Successfully"
    }


# CREATE FIRST HR


@app.post("/firsthr")
def create_first_hr(emp: EmployeeCreate,db: Session = Depends(get_db)):

    stmt = select(employee)

    count = len(
        db.execute(stmt).fetchall()
    )

    if count > 0:
        return {
            "msg": "HR Already Exists"
        }

    corp_mail = (
        emp.last_name[0]
        + emp.first_name
        + "@MiracleSoft.com"
    )

    username = (
        emp.first_name[0]
        + emp.last_name
    )

    now = datetime.now()

    password = (
        emp.first_name[:2]
        + emp.last_name[-2:]
        + "@"
        + str(now.day)
        + str(now.hour)
        + str(now.minute)
    )

    stmt = insert(employee).values(
        FirstName=emp.first_name,
        LastName=emp.last_name,
        Age=emp.age,
        Salary=emp.salary,
        Designation="H",
        PersonalMail=emp.personal_mail,
        CorporateEmail=corp_mail,
        PhoneNumber=emp.phone,
        EmployeeUserName=username,
        Password=password,
        DateOfBirth=emp.dob,
        DateOfJoining=emp.doj
    )

    db.execute(stmt)
    db.commit()

    return {
        "msg": "First HR Created Successfully",
        "username": username,
        "password": password,
        "corporate_mail": corp_mail
    }


# LOGIN

class Login(BaseModel):
    username: str
    password: str
    designation: str


@app.post("/login")
def login(user: Login,db: Session = Depends(get_db)):

    stmt = select(employee).where(
        employee.c.EmployeeUserName == user.username,
        employee.c.Password == user.password,
    )

    data = db.execute(stmt).fetchone()

    if data is None:
        return {
            "msg": "Invalid Username or Password"
        }

    return {
        "msg": "Login Successful",
    }


# ADD EMPLOYEE

@app.post("/employee")
def add_employee(
    emp: EmployeeAddRequest,
    db: Session = Depends(get_db)
):

    # Check Login Credentials

    stmt = select(employee).where(
        employee.c.EmployeeUserName == emp.login_username,
        employee.c.Password == emp.login_password
    )

    logged_user = db.execute(stmt).fetchone()

    if logged_user is None:
        return {
            "msg": "Invalid Username or Password"
        }

    # Check HR Access

    if logged_user.Designation != "H":
        return {
            "msg": "Access Denied. Only HR Can Add Employees"
        }

    # Validate Designation

    stmt = select(roles).where(
        roles.c.RoleId == emp.designation
    )

    role_check = db.execute(stmt).fetchone()

    if role_check is None:
        return {
            "msg": "Invalid Designation"
        }

    # Generate Corporate Mail

    corp_mail = (
        emp.last_name[0]
        + emp.first_name
        + "@MiracleSoft.com"
    )

    # Generate Username

    username = (
        emp.first_name[0]
        + emp.last_name
    )

    # Generate Password

    now = datetime.now()

    password = (
        emp.first_name[:2]
        + emp.last_name[-2:]
        + "@"
        + str(now.day)
        + str(now.hour)
        + str(now.minute)
    )

    # Insert Employee

    stmt = insert(employee).values(
        FirstName=emp.first_name,
        LastName=emp.last_name,
        Age=emp.age,
        Salary=emp.salary,
        Designation=emp.designation,
        PersonalMail=emp.personal_mail,
        CorporateEmail=corp_mail,
        PhoneNumber=emp.phone,
        EmployeeUserName=username,
        Password=password,
        DateOfBirth=emp.dob,
        DateOfJoining=emp.doj
    )

    db.execute(stmt)

    db.commit()

    return {
        "msg": "Employee Inserted Successfully",
        "username": username,
        "password": password,
        "corporate_mail": corp_mail
    }


# GET ALL EMPLOYEES

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):

    stmt = select(employee)

    data = db.execute(stmt).fetchall()

    return [
        dict(row._mapping)
        for row in data
    ]


# GET EMPLOYEE BY ID

@app.get("/employee/{id}")
def get_employee(
    id: int,
    db: Session = Depends(get_db)
):

    stmt = select(employee).where(
        employee.c.EmpId == id
    )

    data = db.execute(stmt).fetchone()

    if data is None:
        return {"msg": "Employee Not Found"}

    return dict(data._mapping)


# UPDATE EMPLOYEE

@app.put("/employee/{id}")
def update_employee(
    id: int,
    emp: EmployeeCreate,
    db: Session = Depends(get_db)
):

    stmt = update(employee).where(
        employee.c.EmpId == id
    ).values(
        FirstName=emp.first_name,
        LastName=emp.last_name,
        Age=emp.age,
        Salary=emp.salary,
        Designation=emp.designation,
        PersonalMail=emp.personal_mail,
        PhoneNumber=emp.phone,
        DateOfBirth=emp.dob,
        DateOfJoining=emp.doj
    )

    db.execute(stmt)
    db.commit()

    return {
        "msg": "Employee Updated Successfully"
    }


# DELETE EMPLOYEE

@app.delete("/employee/{id}")
def delete_employee(
    id: int,
    db: Session = Depends(get_db)
):

    stmt = delete(employee).where(
        employee.c.EmpId == id
    )

    db.execute(stmt)
    db.commit()

    return {
        "msg": "Employee Deleted Successfully"
    }