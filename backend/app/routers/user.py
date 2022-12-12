from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from app import schemas, utils, models
from app.database import get_db
from sqlalchemy.orm import Session
#from app.psycopgdb import db

from fastapi.params import Body
import psycopg

router = APIRouter(prefix="/users", tags=['Users'])

# creating user
@router.post("/", response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    # hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # db.cursor.execute(
    #     """
    #     INSERT INTO users (email, password)
    #     VALUES (%s, %s)
    #     RETURNING *
    #     """, (user.email, user.password)
    # )
    # new_user = db.cursor.fetchone()
    # db.conn.commit()

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # db.cursor.execute(
    #     """
    #     SELECT * FROM users WHERE id = %s
    #     """, (id,)
    # )
    # user = db.cursor.fetchone()
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found")
    return user