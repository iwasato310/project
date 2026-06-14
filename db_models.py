from sqlalchemy import Column, Integer, String
from database import Base

class ItemDB(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)