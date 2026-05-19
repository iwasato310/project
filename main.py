from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# FastAPIアプリ作成
app = FastAPI()

# SQLite DBファイル名
DB_NAME = "items.db"

# POST /echo 用のJSON型定義
class User(BaseModel):
    # {"name": "..."} の name
    name: str

# POST /items 用のJSON型定義
class Item(BaseModel):
    # item名
    name: str

# DB初期化処理
def init_db():
    # SQLite DBへ接続
    conn = sqlite3.connect(DB_NAME)
    # SQL実行用cursor作成
    cursor = conn.cursor()

    # itemsテーブル作成
    # 存在していれば何もしない
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        '''
    )
    # DBへ保存確定
    conn.commit()
    # DB接続終了
    conn.close()

# アプリ起動時にDB初期化
init_db()

# GET /
# 動作確認用API
@app.get("/")
def read_root():
    return {"message": "Hello Docker FastAPI"}

# GET /hello/{name}
# URLからnameを受け取るAPI
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

# POST /echo
# JSONを受け取り、そのまま返すAPI
@app.post("/echo")
def echo_user(user: User):
    return {"message": f"Hello {user.name}"}

# POST /items
# itemをDBへ保存するAPI
@app.post("/items")
def create_item(item: Item):
    # SQLite DBへ接続
    conn = sqlite3.connect(DB_NAME)
    # SQL実行用cursor作成
    cursor = conn.cursor()

    # itemsテーブルへINSERT
    # ? を使うことでSQL Injectionを防止
    cursor.execute(
        "INSERT INTO items (name) VALUES (?)", 
        (item.name,)
    )

    # DBへ保存確定
    conn.commit()
    # INSERTされた行のid取得
    item_id = cursor.lastrowid
    # DB接続終了
    conn.close()

    # JSON Response返却
    return {
        "id": item_id, 
        "name": item.name
    }

# GET /items
# 保存済みitem一覧を返すAPI
@app.get("/items")
def list_items():
    # SQLite DBへ接続
    conn = sqlite3.connect(DB_NAME)
    # SQL実行用cursor作成
    cursor = conn.cursor()

    # itemsテーブルから全件取得
    cursor.execute(
        "SELECT id, name FROM items"
    )
    # SQL結果を全件取得
    rows = cursor.fetchall()

    # DB接続終了
    conn.close()

    # SQLite結果をJSON形式へ変換
    # 例:
    # (1, "apple")
    # ↓
    # {"id": 1, "name": "apple"}
    return [{"id": row[0], "name": row[1]} for row in rows]