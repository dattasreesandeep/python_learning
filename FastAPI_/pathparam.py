from fastapi import FastAPI

app = FastAPI()

@app.get('/data/{item_id}/{item_name}/{item_price}')

def get_data(item_id:int,item_name:str,item_price:float):
    return {'id':item_id,'name':item_name,'price':item_price}