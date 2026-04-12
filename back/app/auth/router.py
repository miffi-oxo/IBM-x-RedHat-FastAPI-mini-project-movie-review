from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.models.users import User
from app.core.security import create_access_token, verify_password, hash_password
from pydantic import BaseModel
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return {
        "username": current_user.user_name,
        "email": current_user.email
    }

@router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # username 중복 체크
    result = await db.execute(
        select(User).where(User.user_name == user.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디")

    # email 중복 체크 (추가!)
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일")

    hashed_pw = hash_password(user.password)

    new_user = User(
        user_name=user.username,
        email=user.email,
        password=hashed_pw
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"msg": "회원가입 완료"}

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.user_name == user.username)
    )
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.user_name})

    return {"access_token": token, "token_type": "bearer"}