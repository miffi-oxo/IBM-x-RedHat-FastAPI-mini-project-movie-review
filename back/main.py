import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.concurrency import asynccontextmanager
from app.db.database import Base, async_engine



load_dotenv(dotenv_path=".env")

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app=FastAPI(lifespan=lifespan)





if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)