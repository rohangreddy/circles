from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# pydantic models allow for data being sent in by frontend to match up with the expected schema
# extends pydantic BaseModel class to represent a post object
# fastapi uses this schema definition to validate data being sent by post requests

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # enable this if using ORM
    class Config:
       orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    # enable this if using ORM
    class Config:
       orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Credentials(BaseModel):
    email: EmailStr
    password: str

    # enable this if using ORM
    class Config:
       orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
       orm_mode = True

