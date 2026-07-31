from sqlalchemy import Column, DateTime, Integer, String, func
from database import Base

class ItemDB(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)

    # 登録日時
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # アイテムの状態
    status = Column(String, nullable=False, server_default='active')