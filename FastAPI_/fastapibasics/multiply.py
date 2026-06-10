from fastapi import FastAPI

app = FastAPI()

@app.get('/data/{num1}')

def add(num1:int,num2:int):
    return {'mul': "multiplication of 2 numbers",'multiply': num1*num2 }