from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Post, Author
from .schemas import PostBase, AuthorBase, PostUpdate
from sqlalchemy import update, delete


async def create_post(db: AsyncSession, post: PostBase):
    db_item = Post(title=post.title, text=post.text, author_id=post.author_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def get_all_posts(db: AsyncSession):
    result = await db.execute(select(Post))
    return result.scalars()


async def update_post(db: AsyncSession, post_id: int, update_data: PostUpdate):
    post = await get_post(db, post_id)
    if post:
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(post, key, value)
        await db.commit()
        await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post_id: int):
    post = await get_post(db, post_id)
    if not post:
        return False
    await db.delete(post)
    await db.commit()
    return True


async def get_all_authors(db: AsyncSession):
    result = await db.execute(select(Author))
    return result.scalars()



async def get_author(db: AsyncSession, author_id: int):
    result = await db.execute(select(Author).where(Author.id == author_id))
    return result.scalar_one_or_none()


async def create_author(db: AsyncSession, author: Author):
    db_item = Author(first_name=author.first_name, second_name=author.second_name)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item