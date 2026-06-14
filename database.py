import os
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

# import psycopg2


# 環境変数からDB接続情報を取得
#
# Docker Composeでは
# DB_HOST=db
#
# ローカル実行時は
# localhost を使用
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")

# SQLAlchemy用のDB接続URL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:5432/{DB_NAME}"
)


# DB接続エンジン
engine = create_engine(DATABASE_URL)

# DBセッション作成用
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# DBモデルの基底クラス
Base = declarative_base()


def init_db_with_retry(retries=10, wait_seconds=2):
    """
    DB起動待ち付きでテーブルを作成する
    """

    for attempt in range(retries):
        try:
            # db_models.py 内の Base継承クラスを読み込むためにimport
            import db_models  # noqa: F401

            # テーブル作成
            Base.metadata.create_all(bind=engine)
            return

        except OperationalError:
            print(
                f"DB connection failed. "
                f"retry={attempt + 1}/{retries}"
            )

            if attempt == retries - 1:
                raise

            time.sleep(wait_seconds)


def get_db():
    """
    FastAPIで使うDBセッションを取得する
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

