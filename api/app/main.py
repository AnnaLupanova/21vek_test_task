from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import AsyncSessionLocal, engine, Base
from . import models
from . import schemas
from . import crud
from . import logging
from typing import List

logger = logging.get_logger("./api_log.log")

app = FastAPI()

async def init_data():
    INIT_AUTHORS = [
        {"first_name": "Ivan", "second_name": "Petrov"},
        {"first_name": "Jon", "second_name": "Ivanov"},
        {"first_name": "Anna", "second_name": "Sokolova"},
    ]

    async with AsyncSessionLocal() as session:
        for author in INIT_AUTHORS:
            new_author = models.Author(**author)
            session.add(new_author)
        await session.commit()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_data()


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/posts/", response_model=schemas.PostBase)
async def create_post(post: schemas.PostBase, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating post: {post.title}")
    return await crud.create_post(db=db, post=post)


@app.get("/posts/", response_model=List[schemas.Post])
async def get_all_posts(db: AsyncSession = Depends(get_db)):
    logger.info(f"Reading all posts")
    return await crud.get_all_posts(db=db)


@app.get("/posts/{post_id}", response_model=schemas.Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Reading post with ID: {post_id}")
    db_post = await crud.get_post(db=db, post_id=post_id)
    if db_post is None:
        logger.warning(f"Post with ID {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.put("/posts/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, post: schemas.PostUpdate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Updating post with ID: {post_id}")
    db_post = await crud.update_post(db=db, post_id=post_id, update_data=post)
    if db_post is None:
        logger.warning(f"Post with ID {post_id} not found")
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: AsyncSessionLocal = Depends(get_db)):
    logger.info(f"Deleting post with ID: {post_id}")
    result = await crud.delete_post(db, post_id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}


@app.get("/authors/", response_model=List[schemas.Author])
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    logger.info(f"Reading all posts")
    return await crud.get_all_authors(db=db)


@app.get("/authors/{author_id}", response_model=schemas.Author)
async def read_author(author_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Reading author with ID: {author_id}")
    author = await crud.get_author(db=db, author_id=author_id)
    if author is None:
        logger.warning(f"Author with ID {author_id} not found")
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
async def create_author(author: schemas.AuthorBase, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating author: {author.first_name}")
    return await crud.create_author(db=db, author=author)
