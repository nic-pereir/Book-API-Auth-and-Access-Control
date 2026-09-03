from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

# AUTHOR

class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# BOOK

class BookBase(BaseModel):
    title: str
    genre: Optional[str] = None
    year_publication: Optional[int] = None


class BookCreate(BookBase):
    author_id: Optional[int] = None


class BookOut(BookBase):
    id: int
    author_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class AuthorWithBooks(AuthorOut):
    books: list[BookOut] = []


# USER

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    # Note there is no "password" or "hashed_password" field here on purpose:
    # this schema controls what the API is allowed to send back to the client.
    id: int
    name: str
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)


# AUTH

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
