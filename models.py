from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(
        description="ユーザー名", 
        json_schema_extra={"example": "Taro"}
    )

class Item(BaseModel):
    name: str = Field(
        description="アイテム名",
        json_schema_extra={"example": "apple"},
    )