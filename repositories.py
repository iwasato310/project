from sqlalchemy.orm import Session

from db_models import ItemDB
from models import ItemCreate

def create_item(db: Session, item: ItemCreate) -> ItemDB:
    # SQLAlchemyのDBモデルを作成
    db_item = ItemDB(name=item.name)

    # DBセッションに追加
    db.add(db_item)

    # DBへ保存確定
    db.commit()

    # 採番されたIDなどを反映
    db.refresh(db_item)

    return db_item


def list_items(db: Session):
    # itemsテーブルをID順で全件取得
    return db.query(ItemDB).order_by(ItemDB.id).all()


def get_item(db: Session, item_id: int):
    # 指定IDのitemを1件取得
    return db.query(ItemDB).filter(ItemDB.id == item_id).first()


def update_item(db: Session, item_id: int, item: ItemCreate):
    # 更新対象を取得
    db_item = get_item(db, item_id)

    # 存在しない場合は None を返す
    if db_item is None:
        return None

    # 値を更新
    db_item.name = item.name

    # DBへ保存確定
    db.commit()

    # 更新後の値を反映
    db.refresh(db_item)

    return db_item


def delete_item(db: Session, item_id: int):
    # 削除対象を取得
    db_item = get_item(db, item_id)

    # 存在しない場合は None を返す
    if db_item is None:
        return None

    # DBから削除
    db.delete(db_item)

    # 削除を確定
    db.commit()

    return db_item