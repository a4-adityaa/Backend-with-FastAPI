from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()
my_posts = [{"title": "title of post 1", "content":"Content of post 1", "id": 1}, {"title":"favourite foods", "contetnt":"I like pizza", "id":2}]

# if two methods are same with same pasth, the first found will be represented (order matters)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True   # optional
    rating: Optional[int] = None  # optional

# not the appropriate way to get content by id:
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in  enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hey how are you?"}


@app.get("/posts")
def get_data():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPosts(post: Post):  # paylaod is a variable here who stores data from body in form of dict
    post_dict = post.dict()
    post_dict['id'] = randrange(1,10000)
    my_posts.append(post.dict())
    return {"data": post_dict}


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"details": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}
    
    return {"post_details": post}

# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has the required id
    # my_post.pop(index)
    
    index= find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update Post