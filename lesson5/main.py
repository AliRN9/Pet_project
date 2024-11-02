from typing import Optional, List, Dict, Annotated

from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as BbUSer, PostCreate, PostResponse

app = FastAPI()



Base.metadata.create_all(engine)


def get_db() -> Session:
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=BbUSer)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> BbUSer:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.get("/users/", response_model=List[BbUSer])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(User).all()

# users = [
#     {"id": 1, "name": "Alex", "age": 35},
#     {"id": 2, "name": "Nike", "age": 12},
#     {"id": 3, "name": "Kris", "age": 26},
# ]
#
# posts = [
#     {"id": 1, "title": "New1", "body": "Text 1", 'author': users[1]},
#     {"id": 2, "title": "New2", "body": "Text 2", 'author': users[0]},
#     {"id": 3, "title": "New3", "body": "Text 3", 'author': users[2]},
# ]

# @app.post('/users/add')
# async def user_add(user: Annotated[UserCreate, Body(..., example={"name": "UserName", "age": 1})]) -> User:
#     new_id = len(users) + 1
#     new_user = {"id": new_id, "name": user.name, "age": user.age}
#     users.append(new_user)
#     return User(**new_user)
#
#
# @app.post("/items/add")
# async def add_item(post: PostCreate) -> Post:
#     # author = posts['author'][post.author_id]
#     author = next((user for user in users if user["id"] == post.author_id), None)
#     if author is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     new_post_id = len(posts) + 1
#     new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
#     posts.append(new_post)
#     print(Post(**new_post))
#     return Post(**new_post)
#
#
# @app.put("/items/edit/{post_id}")
# async def edit_item(new_post: Post) -> Post:
#     # author = posts['author'][post.author_id]
#     number = next((i for i, post in enumerate(posts) if post["id"] == new_post.id), None)
#     if number is None:
#         raise HTTPException(status_code=404, detail="post not found")
#
#     new_post = {'id': new_post.id, 'title': new_post.title, 'body': new_post.body, 'author': new_post.author}
#     posts[number] = new_post
#
#     return Post(**new_post)

#
# @app.delete("/items/delete/{post_id}")
# async def delete_item(post_id: int) -> Dict:
#     # author = posts['author'][post.author_id]
#     number = next((i for i, post in enumerate(posts) if post["id"] == post_id), None)
#     if number is None:
#         raise HTTPException(status_code=404, detail="post not found")
#
#     posts.pop(number)
#     return {'id': post_id, 'status': 'deleted'}
#
#
# @app.get("/items")
# async def items() -> List[Post]:
#     print([Post(**post) for post in posts])
#     return [Post(**post) for post in posts]
#
#
# @app.get("/items/{post_id}")
# async def items(post_id: Annotated[int, Path(title='Здесь указывается id поста', ge=1, lt=100)]) -> Post:
#     for post in posts:
#         if post["id"] == post_id:
#             return Post(**post)
#     raise HTTPException(status_code=404, detail="Post not found")
#
#
# @app.get("/search")
# async def search(post_id: Annotated[Optional[int], Query(title='ID of post to search for', ge=1, le=50)]) -> Dict[
#     str, Optional[Post]]:
#     if post_id is None:
#         return {"data": None}
#     for post in posts:
#         if post["id"] == post_id:
#             return {'data': Post(**post)}
#     raise HTTPException(status_code=404, detail="Post not found")