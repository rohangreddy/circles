from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from app import schemas, models
from app.database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import oauth2
#from app.psycopgdb import db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags = ['Posts'])

@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user: dict = Depends(oauth2.get_current_user), 
              limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    # db.cursor.execute("""SELECT * FROM posts""")
    # posts = db.cursor.fetchall()
    print(user)
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


# id field is a path parameter passed by user that backend uses
# to find individual post
@router.get("/{id}", response_model = schemas.PostOut)
# specifying function parameter as int allows fastapi to validate data sent by user automatically
def get_post(id: int, db: Session = Depends(get_db), user: dict = Depends(oauth2.get_current_user)):
    # db.cursor.execute(
    #     """SELECT * FROM posts WHERE id = %s """, (id,))
    # post = db.cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return post

# creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                user: dict = Depends(oauth2.get_current_user)):
    # db.cursor.execute(
    #     """INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *""", (post.title, post.content, post.published))
    # new_post = db.cursor.fetchone()
    # pushes the changes
    # db.conn.commit()
    new_post = models.Post(user_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# deleting post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user: dict = Depends(oauth2.get_current_user)):
    # db.cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # post = db.cursor.fetchone()
    # db.conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updating a post
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user: dict = Depends(oauth2.get_current_user)):
    # db.cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #     (post.title, post.content, post.published, id))
    # updated_post = db.cursor.fetchone()
    # db.conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    if updated_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()