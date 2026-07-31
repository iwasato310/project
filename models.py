from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class User(BaseModel):
    name: str = Field(
        description="ユーザー名", 
        json_schema_extra={"example": "Taro"}
    )

# POST /items で受け取るデータ
class ItemCreate(BaseModel):
    name: str = Field(
        description="アイテム名",
        json_schema_extra={"example": "apple"},
    )

# APIから返すデータ
class ItemResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)
