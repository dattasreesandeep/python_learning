from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class calculate(BaseModel):
    num1:int
    num2:int

@app.post('/data/')

def division(obj:calculate):
    try:
        if obj.num2==0:
            raise ZeroDivisionError
    except ZeroDivisionError:
        print()
    return {'num1':obj.num1,'num2':obj.num2,'div': obj.num1/obj.num2}

