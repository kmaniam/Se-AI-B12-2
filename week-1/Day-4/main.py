from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application"}


@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}!"}