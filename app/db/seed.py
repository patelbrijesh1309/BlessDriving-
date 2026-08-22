import asyncio

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.role import Role


DEFAULT_ROLES = [
    {
        "name": "ADMIN",
        "description": "System administrator with full access.",
    },
    {
        "name": "INSTRUCTOR",
        "description": "Driving instructor with instructor-specific access.",
    },
    {
        "name": "STUDENT",
        "description": "Driving student with student-specific access.",
    },
]


async def seed_roles():
    async with AsyncSessionLocal() as db:

        for role_data in DEFAULT_ROLES:

            result = await db.execute(
                select(Role).where(
                    Role.name == role_data["name"]
                )
            )

            existing_role = result.scalar_one_or_none()

            if existing_role:
                print(
                    f"Role already exists: {role_data['name']}"
                )
                continue

            role = Role(
                name=role_data["name"],
                description=role_data["description"],
            )

            db.add(role)

            print(
                f"Creating role: {role_data['name']}"
            )

        await db.commit()


async def main():
    await seed_roles()


if __name__ == "__main__":
    asyncio.run(main())