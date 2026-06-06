from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(
        description="ユーザー名", 
        example=["Taro"]
    )

class Item(BaseModel):
    name: str = Field(
        description="アイテム名",
        example=["apple"]
    )