#python -m uvicorn firstapi:main --reload 
from fastapi import FastAPI

main = FastAPI()

@main.get("/")
def read_root():
    return {"Hello": "World"}

@main.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@main.post("/items")
def create_item():
    return {"message": "Item created"}

@main.put("/items/{item_id}")
def update_item(item_id: int):
    return {"message": "Item updated", "item_id": item_id}

@main.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "Item deleted", "item_id": item_id}