from sqlalchemy import Table, Column, Integer, String, Float, Date, ForeignKey
from database import metadata

roles = Table(
    "Roles",
    metadata,

    Column("RoleId", String(1), primary_key=True),
    Column("RoleName", String(50), unique=True)
)

employee = Table(
    "Employee",
    metadata,

    Column("EmpId", Integer, primary_key=True, autoincrement=True),

    Column("FirstName", String(50)),
    Column("LastName", String(50)),
    Column("Age", Integer),
    Column("Salary", Float),

    Column(
        "Designation",
        String(1),
        ForeignKey("Roles.RoleId")
    ),

    Column("PersonalMail", String(50)),
    Column("CorporateEmail", String(50)),
    Column("PhoneNumber", Integer),

    Column("EmployeeUserName", String(50)),
    Column("Password", String(50)),

    Column("DateOfBirth", Date),
    Column("DateOfJoining", Date)
)