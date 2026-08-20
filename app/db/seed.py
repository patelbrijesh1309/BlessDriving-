import asyncio

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.language import Language

DEFAULT_LANGUAGES = [
    {"code": "EN", "name": "English"},
    {"code": "FR", "name": "French"},
    {"code": "AR", "name": "Arabic"},
    {"code": "ES", "name": "Spanish"},
    {"code": "ZH", "name": "Mandarin"},
]


async def seed_languages():
    async with AsyncSessionLocal() as session:
        for item in DEFAULT_LANGUAGES:
            result = await session.execute(
                select(Language).where(Language.code == item["code"])
            )

            exists = result.scalar_one_or_none()

            if not exists:
                session.add(Language(**item))

        await session.commit()


async def main():
    await seed_languages()


if __name__ == "__main__":
    asyncio.run(main())