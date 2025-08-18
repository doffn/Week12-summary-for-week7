from pydantic import BaseModel

class TopProduct(BaseModel):
    object_class: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    count: int

class MessageSearchResult(BaseModel):
    id: int
    text: str
    channel: str
    date: str