from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sqlalchemy import insert,update,delete,select
from sqlalchemy.orm import Session

from database import (
    engine,
    SessionLocal,
    metadata
)

from model import persondata

app = FastAPI()

metadata.create_all(bind=engine)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

class CreatePerson(BaseModel):

    id: int

    name: str


@app.post("/add/")
def new_person(add: CreatePerson,db: Session = Depends(get_db)):
    stmt = insert(persondata).values(
        pid=add.id,
        pname=add.name
    )

    db.execute(stmt)

    db.commit()

    return {

        "msg": "created",
        "id": add.id,
        "name": add.name

    }


@app.get('/read/')

def read_person(db: Session = Depends(get_db)):

    stmt = select(persondata)

    result=db.execute(stmt).mappings().all()

    return result



@app.put("/update/")
def update_person(update1: CreatePerson,db: Session = Depends(get_db)):
    stmt = update(persondata).values(pname=update1.name).where(persondata.c.pid == update1.id)

    db.execute(stmt)

    db.commit()

    return {

        "msg": "updated",
        "id": update1.id,
        "name": update1.name

    }


class DeletePerson(BaseModel):

    id: int


@app.delete("/delete/")
def delete_person(delete1:DeletePerson ,db: Session = Depends(get_db)):
    stmt = delete(persondata).where(persondata.c.pid == delete1.id)

    db.execute(stmt)

    db.commit()

    return {

        "msg": "deleted",
        "id": delete1.id,

    }

