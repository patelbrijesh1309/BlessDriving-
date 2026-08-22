import asyncio

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.role import Role
from app.models.user import User


ADMIN_EMAIL = "admin@blessdriving.com"
ADMIN_PASSWORD = "Admin@123"


async def bootstrap_admin():
    async with AsyncSessionLocal() as db:

        # Check if admin already exists
        result = await db.execute(
            select(User).where(User.email == ADMIN_EMAIL)
        )
        admin = result.scalar_one_or_none()

        if admin:
            print("Admin already exists.")
            return

        # Get ADMIN role
        role_result = await db.execute(
            select(Role).where(Role.name == "ADMIN")
        )
        admin_role = role_result.scalar_one_or_none()

        if admin_role is None:
            print("ADMIN role not found.")
            return

        # Create admin user
        admin = User(
            email=ADMIN_EMAIL,
            password_hash=hash_password(ADMIN_PASSWORD),
            first_name="System",
            last_name="Administrator",
            is_active=True,
        )

        admin.roles.append(admin_role)

        db.add(admin)
        await db.commit()

        print("Bootstrap admin created successfully.")
        print(f"Email: {ADMIN_EMAIL}")
        print(f"Password: {ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(bootstrap_admin())