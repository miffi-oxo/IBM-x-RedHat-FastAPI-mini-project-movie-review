import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import Base, async_engine, get_db
from app.db.models.movies import Movie
from app.db.models.reviews import Review
from app.db.scheme.movies import MovieCreate
from app.db.scheme.reviews import ReviewCreate
from app.auth.router import router as auth_router
from app.auth.dependencies import get_current_user
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

@app.post("/movies")
async def create_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    await db.commit()
    await db.refresh(new_movie)
    return new_movie



@app.get("/movies")
async def get_movies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie))
    return result.scalars().all()



@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.mov_id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie



@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, movie: MovieCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.mov_id == movie_id))
    existing_movie = result.scalar_one_or_none()

    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    existing_movie.mov_name = movie.mov_name
    existing_movie.mov_descript = movie.mov_descript
    existing_movie.genre = movie.genre

    await db.commit()
    await db.refresh(existing_movie)

    return existing_movie



@app.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Review).where(Review.rev_id == review_id)
    )
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # 🔥 본인만 삭제 가능
    if review.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="권한 없음")

    await db.delete(review)
    await db.commit()

    return {"message": "deleted"}



@app.post("/reviews")
async def create_review(
    review: ReviewCreate,
    user = Depends(get_current_user),  # 🔥 추가
    db: AsyncSession = Depends(get_db)
):
    new_review = Review(
        **review.dict(),
        user_id=user.user_id  # 🔥 핵심
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return new_review



@app.get("/reviews")
async def get_reviews(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Review).where(Review.mov_id == movie_id)
    )
    return result.scalars().all()



@app.delete("/reviews/{review_id}")
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Review).where(Review.rev_id == review_id)
    )
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    await db.delete(review)
    await db.commit()

    return {"message": "deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)