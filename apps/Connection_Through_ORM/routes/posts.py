from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    )


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post2).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPosts(post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # new_post = models.Post2(title= post.title, content= post.content, published=post.published)
    new_post = models.Post2(owner_id =current_user.id, **post.dict()) # derefrencing the post class in dictionary form.

    db.add(new_post) # add in log to be commited
    db.commit()  # commits the changes 
    db.refresh(new_post) # returning the newly created post

    return new_post
    

# get post by id.
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post2).filter(models.Post2.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {id} not found")
    
    return post

# delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post2).filter(models.Post2.id == id)
    post = post_query.first()

    if post  == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autharized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update Post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post2).filter(models.Post2.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autharized to perform requested action.")
    

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()