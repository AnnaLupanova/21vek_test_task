from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str
    author_id: int


class PostUpdate(BaseModel):
    title: str
    text: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    first_name: str
    second_name: str


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
