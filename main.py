from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

# if two methods are same with same pasth, the first found will be represented (order matters)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Hey how are you?"}


@app.get("/posts")
def get_data():
    return {"data": "This is your post.."}


@app.post("/createPost")
def createPost(new_post: Post):  # paylaod is a variable here who stores data from body in form of dict
    print(new_post.title)
    return {"data": new_post}