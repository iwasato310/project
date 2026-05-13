from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello Docker FastAPI"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/echo")
def echo_user(user: User):
    return {"message": f"Hello {user.name}"}