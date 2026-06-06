from fastapi import FastAPI, HTTPException

from database import get_connection, init_db
from models import Item, User

# FastAPIアプリ作成
app = FastAPI()

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
@app.post(
    "/items",
    summary="アイテムを登録する",
    description="新しいアイテムをPostgreSQLへ保存します"
)
def create_item(item: Item):
    conn = get_connection()
    cursor = conn.cursor()

    # itemsテーブルへINSERT
    cursor.execute(
        "INSERT INTO items (name) VALUES (%s) RETURNING id",
        (item.name,),
    )

    # INSERTされた行のid取得
    item_id = cursor.fetchone()[0]

    # DBへの変更を確定
    conn.commit()
    # SQL実行用カーソルを閉じる
    cursor.close()
    # DB接続を終了
    conn.close()

    # JSON Response返却
    return {
        "id": item_id, 
        "name": item.name
    }

# GET /items
# 保存済みitem一覧を返すAPI
@app.get(
    "/items",
    summary="アイテム一覧取得",
    description="保存済みアイテムをすべて返します"
)
def list_items():
    conn = get_connection()
    cursor = conn.cursor()

    # itemsテーブルから全件取得
    cursor.execute(
        "SELECT id, name FROM items ORDER BY id"
    )
    # SQL結果を全件取得
    rows = cursor.fetchall()

    # SQL実行用カーソルを閉じる
    cursor.close()
    # DB接続を終了
    conn.close()

    # 結果をJSON形式へ変換
    # 例:
    # (1, "apple")
    # ↓
    # {"id": 1, "name": "apple"}
    # 補足
    #　Python のリスト内包表記は 「作るもの → for 文」 の順番で書くルール
    # 例えば、以下のようなコードはリスト内包表記ではなく、普通のfor文で書いている例
    # result = []
    # for row in rows:
    #     result.append({"id": row[0], "name": row[1]})
    # return result
    return [{"id": row[0], "name": row[1]} for row in rows]

# PUT /items/{item_id}
# itemをDBから更新するAPI
@app.put(
    "/items/{item_id}",
    summary="アイテム更新",
    description="指定したIDのアイテム名を更新します"
)
def update_item(item_id: int, item: Item):
    conn = get_connection()
    cursor = conn.cursor()

    # 指定IDのitemを更新
    cursor.execute(
        "UPDATE items SET name = %s WHERE id = %s",
        (item.name, item_id),
    )

    updated_count = cursor.rowcount

    # DBへの変更を確定
    conn.commit()
    # SQL実行用カーソルを閉じる
    cursor.close()
    # DB接続を終了
    conn.close()

    # 存在しないIDだった場合
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"id": item_id, "name": item.name}

# DELETE /items/{item_id}
# itemをDBから削除するAPI
@app.delete(
    "/items/{item_id}",
    summary="アイテム削除",
    description="指定したIDのアイテムを削除します"
)
def delete_item(item_id: int):

    # DB接続
    conn = get_connection()
    cursor = conn.cursor()

    # 指定IDのitemを削除
    cursor.execute(
        "DELETE FROM items WHERE id = %s",
        (item_id,)
    )

    # 何件削除したか取得
    deleted_count = cursor.rowcount

    # DBへの変更を確定
    conn.commit()
    # SQL実行用カーソルを閉じる
    cursor.close()
    # DB接続を終了
    conn.close()

    # 存在しないIDだった場合
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted", "id": item_id}