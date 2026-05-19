from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


app = FastAPI()

DB_NAME = "items.db"


class User(BaseModel):
    name: str

class Item(BaseModel):
    name: str


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()



@app.get("/")
def read_root():
    return {"message": "Hello Docker FastAPI"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/echo")
def echo_user(user: User):
    return {"message": f"Hello {user.name}"}

@app.post("/items")
def create_item(item: Item):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (item.name,))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {"id": item_id, "name": item.name}

@app.get("/items")
def list_items():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1]} for row in rows]