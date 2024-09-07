from pydantic import BaseModel
from typing import Optional


# Pydantic model for User schema
class UserBase(BaseModel):
    username: str
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to interact with SQLAlchemy objects


# Pydantic model for Book schema
class BookBase(BaseModel):
    title: str
    author: str
    is_borrowed: Optional[bool] = False


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True
