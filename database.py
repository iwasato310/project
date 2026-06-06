import os
import time

import psycopg2

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


def get_connection():
    """
    PostgreSQLへ接続する

    Returns:
        psycopg2 connection
    """

    return psycopg2.connect(
        host=DB_HOST,
        port=5432,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def get_connection_with_retry(
    retries=10,
    wait_seconds=2,
):
    """
    PostgreSQL接続リトライ

    GitHub Actions や Docker Compose では

        app起動
        ↓
        PostgreSQL起動中

    となることがある。

    DB起動完了まで待機しながら再接続する。
    """

    for attempt in range(retries):

        try:
            return get_connection()

        except psycopg2.OperationalError:

            print(
                f"DB connection failed. "
                f"retry={attempt + 1}/{retries}"
            )

            # 最終リトライなら例外を再送出
            if attempt == retries - 1:
                raise

            # 少し待って再試行
            time.sleep(wait_seconds)


def init_db():
    """
    アプリ起動時のDB初期化

    itemsテーブルが存在しなければ作成する。
    """

    # DB接続
    conn = get_connection_with_retry()

    # SQL実行用カーソル取得
    cursor = conn.cursor()

    # テーブル作成
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )

    # DBへの変更を確定
    conn.commit()

    # カーソルを閉じる
    cursor.close()

    # DB接続を終了
    conn.close()