from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.health import check_database
from app.api.students import router as student_router
from app.api.instructors import router as instructor_router
from app.api.auth import router as auth_router
from app.core.dependencies import get_current_user
from app.models.user import User
from app.api.admin import router as admin_router


app = FastAPI(
    title="BlessDriving API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(student_router)
app.include_router(instructor_router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "BlessDriving API",
    }


@app.get("/health/database")
async def database_health(
    db: AsyncSession = Depends(get_db),
):
    connected = await check_database(db)

    return {
        "database": "connected" if connected else "disconnected"
    }

@app.get("/me")
async def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.first_name,
    }