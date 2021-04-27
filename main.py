from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from database.connection import get_db
from database.model import Posts
from schemas.models import Post, UpdatePost

app = FastAPI()


@app.delete("/posts/delete/{id}")
def delete_post(id, db: Session = Depends(get_db)):
    db.query(Posts).filter_by(id=id).delete()
    db.commit()
    return {"message": "successfully completed"}


@app.get("/posts/list/all", response_model=List[Post])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Posts).all()
    return posts


@app.post("/post/create", response_model=Post)
def create_posts(post: Post, db: Session = Depends(get_db)):
    post = Posts(id=post.id, title=post.title, description=post.description)
    db.add(post)
    db.commit()
    return post


@app.get("/posts/read/{id}")
def read_post(id, db: Session = Depends(get_db)):
    post = db.query(Posts).filter_by(uuid=id).one()
    return post


@app.patch("/posts/update", response_model=UpdatePost)
def update_post(post: Post, db: Session = Depends(get_db)):
    found = db.query(Posts).filter_by(uuid=post.id)
    if found is None:
        return {"message": "doesn't exist"}
    else:
        update_query = {Posts.title: post.title, Posts.description: post.description}
        db.query(Posts).filter_by(uuid=post.id).update(update_query)
        db.commit()
        return db.query(Posts).filter_by(uuid=post.id).one()
