from sqlalchemy import Table, Column, Integer, String
from database import metadata

persondata = Table(
    "person",
    metadata,

    Column(
        "pid",
        Integer,
        primary_key=True
    ),

    Column(
        "pname",
        String(50)
    )
)