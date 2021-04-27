from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


class Post(BaseModel):
    id: Optional[UUID]
    title: str
    description: str

    class Config:
        orm_mode = True


class DeletePostResponse(BaseModel):
    detail: str


class UpdatePost(BaseModel):
    detail: str
    post: Optional[Post]

    class Config:
        orm_mode = True
