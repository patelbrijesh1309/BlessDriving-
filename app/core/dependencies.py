from jose import JWTError, jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials.",
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise credentials_exception

    return user

async def require_admin(
    current_user: User = Depends(get_current_user),
):
    if not any(role.name == "ADMIN" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="Admin access required.",
        )

    return current_user


async def require_scheduler(
    current_user: User = Depends(get_current_user),
):
    if not any(role.name == "SCHEDULER" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="Scheduler access required.",
        )

    return current_user


async def require_instructor(
    current_user: User = Depends(get_current_user),
):
    if not any(role.name == "INSTRUCTOR" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="Instructor access required.",
        )

    return current_user


async def require_student(
    current_user: User = Depends(get_current_user),
):
    if not any(role.name == "STUDENT" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="Student access required.",
        )

    return current_user