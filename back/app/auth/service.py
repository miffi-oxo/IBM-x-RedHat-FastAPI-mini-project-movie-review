from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.users import User
from app.core.security import verify_password, hash_password


async def create_user(db: AsyncSession, email: str, password: str):
    hashed_pw = hash_password(password)

    user = User(
        user_name=email,
        email=email,
        password=hashed_pw
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user