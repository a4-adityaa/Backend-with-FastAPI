from pydantic import BaseModel

# class Post(BaseModel):


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass