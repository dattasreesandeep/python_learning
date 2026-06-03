from fastapi import FastAPI

app= FastAPI()

@app.get('/data')

def display(id:int,name:str):
    return {'item_id':id,'item_name':name}