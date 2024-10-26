from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI-Vue Project"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}
