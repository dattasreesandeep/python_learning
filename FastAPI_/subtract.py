from fastapi import FastAPI

app = FastAPI()

@app.get('/data')

def subtract(num1:int,num2:int):
    return {'num1':num1,'num2':num2, 'sub':num1-num2}