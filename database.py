import os
import sqlite3

DB_NAME = os.getenv("DB_NAME", "items.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

# DB初期化処理
def init_db():
    # SQLite DBへ接続
    conn = get_connection()
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