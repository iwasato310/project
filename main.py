import repositories

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import get_db, init_db_with_retry
from models import Item, User

# FastAPIアプリ作成
app = FastAPI()

# アプリ起動時にDB初期化
init_db_with_retry()

# GET /
# 動作確認用API
@app.get("/")
def read_root():
    return {"message": "Hello Docker FastAPI"}

# GET /hello/{name}
# URLの一部を name として受け取るAPI
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

# POST /echo
# JSONで受け取った name を使ってメッセージを返すAPI
@app.post("/echo")
def echo_user(user: User):
    return {"message": f"Hello {user.name}"}

# POST /items
# 新しいitemをDBへ登録するAPI
@app.post(
    "/items",
    summary="アイテムを登録する",
    description="新しいアイテムをPostgreSQLへ保存します"
)
def create_item(
    item: Item, 

    # FastAPIのDependsを使ってDBセッションを取得
    db: Session = Depends(get_db),
):
    db_item = repositories.create_item(db, item)

    # APIレスポンスとして返却
    return {
        "id": db_item.id,
        "name": db_item.name,
    }

# GET /items
# 保存済みitem一覧を取得するAPI
@app.get(
    "/items",
    summary="アイテム一覧取得",
    description="保存済みアイテムをすべて返します"
)
def list_items(
    # DBセッションを取得
    db: Session = Depends(get_db),
):
    # itemsテーブルをid順で全件取得
    items = repositories.list_items(db)

    # 結果をJSON形式へ変換
    # 例:
    # (1, "apple")
    # ↓
    # {"id": 1, "name": "apple"}
    # 補足
    #　Python のリスト内包表記は 「作るもの → for 文」 の順番で書くルール
    # 例えば、以下のようなコードはリスト内包表記ではなく、普通のfor文で書いている例
    # result = []
    # for item in items:
    #     result.append({"id": item.id, "name": item.name})
    # return result
    return [{"id": item.id, "name": item.name} for item in items]

# PUT /items/{item_id}
# itemをDBから更新するAPI
@app.put(
    "/items/{item_id}",
    summary="アイテム更新",
    description="指定したIDのアイテム名を更新します"
)
def update_item(
    item_id: int,
    item: Item,

    # DBセッションを取得
    db: Session = Depends(get_db),
):
    db_item = repositories.update_item(db, item_id, item)

    # 対象が存在しない場合は404を返す
    if db_item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    # 更新後の内容を返却
    return {
        "id": db_item.id,
        "name": db_item.name,
    }

# DELETE /items/{item_id}
# itemをDBから削除するAPI
@app.delete(
    "/items/{item_id}",
    summary="アイテム削除",
    description="指定したIDのアイテムを削除します"
)
def delete_item(
    item_id: int,

    # DBセッションを取得
    db: Session = Depends(get_db),
):
    db_item = repositories.delete_item(db, item_id)

    # 対象が存在しない場合は404を返す
    if db_item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    # 削除結果を返却
    return {
        "message": "Item deleted",
        "id": item_id,
    }