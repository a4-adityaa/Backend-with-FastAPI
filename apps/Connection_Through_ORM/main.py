from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='@arun7048', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)



@app.get("/")
async def root():
    return {"message": "Hey how are you?"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post2).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPosts(post: schemas.PostCreate, db: Session= Depends(get_db)):
    
    # new_post = models.Post2(title= post.title, content= post.content, published=post.published)
    new_post = models.Post2(**post.dict()) # derefrencing the post class in dictionary form.

    db.add(new_post) # add in log to be commited
    db.commit()  # commits the changes 
    db.refresh(new_post) # returning the newly created post

    return new_post
    


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session= Depends(get_db)):

    post = db.query(models.Post2).filter(models.Post2.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {id} not found")
    
    return post

# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session= Depends(get_db)):

    post = db.query(models.Post2).filter(models.Post2.id == id)

    if post.first()  == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update Post
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session= Depends(get_db)):

    post_query = db.query(models.Post2).filter(models.Post2.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    print(len(user.password.encode("utf-8")))

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user