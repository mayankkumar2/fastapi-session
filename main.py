from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from database.model import Posts
from schemas.models import Post, UpdatePost, DeletePostResponse

app = FastAPI()


@app.delete("/posts/delete/{id}", status_code=status.HTTP_200_OK, response_model=DeletePostResponse)
def delete_post(id, db: Session = Depends(get_db)):
    post = db.query(Posts).filter_by(id=id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="doesn't exist")
    print(post)
    db.query(Posts).filter_by(id=id).delete()
    db.commit()
    return DeletePostResponse(detail="deleted successfully")


@app.get("/posts/list/all", status_code=status.HTTP_200_OK, response_model=List[Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Posts).all()
    return posts


@app.post("/posts/create", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: Post, db: Session = Depends(get_db)):
    post = Posts(id=post.id, title=post.title, description=post.description)
    db.add(post)
    db.commit()
    return post


@app.get("/posts/read/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def read_post(id, db: Session = Depends(get_db)):
    post = db.query(Posts).filter_by(id=id).one()
    return post


@app.patch("/posts/update", status_code=status.HTTP_200_OK, response_model=UpdatePost)
def update_post(post: Post, db: Session = Depends(get_db)):
    found = db.query(Posts).filter_by(id=post.id).all()
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="doesn't exist")
    else:
        update_query = {Posts.title: post.title, Posts.description: post.description}
        db.query(Posts).filter_by(id=post.id).update(update_query)
        db.commit()
        return UpdatePost(detail="updated successfully", post=db.query(Posts).filter_by(id=post.id).one())
