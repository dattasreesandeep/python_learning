from fastapi import FastAPI

app = FastAPI()

@app.get('/data/{num1}/{num2}')

def add(num1:int,num2:int):
    return ('addition of 2 numbers','sum=', num1+num2 )