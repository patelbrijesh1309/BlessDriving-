# from fastapi import HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.repositories.instructor_repository import InstructorRepository
# from app.schemas.instructor import InstructorCreate, InstructorUpdate


# class InstructorService:

#     @staticmethod
#     async def create_instructor(
#         db: AsyncSession,
#         data: InstructorCreate,
#     ):
#         existing = await InstructorRepository.get_by_id(db, data.user_id)

#         if existing:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Instructor already exists.",
#             )

#         return await InstructorRepository.create(db, data)

#     @staticmethod
#     async def get_instructor(
#         db: AsyncSession,
#         user_id: int,
#     ):
#         instructor = await InstructorRepository.get_by_id(db, user_id)

#         if not instructor:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Instructor not found.",
#             )

#         return instructor

#     @staticmethod
#     async def get_instructors(db: AsyncSession):
#         return await InstructorRepository.get_all(db)

#     @staticmethod
#     async def update_instructor(
#         db: AsyncSession,
#         user_id: int,
#         data: InstructorUpdate,
#     ):
#         instructor = await InstructorRepository.get_by_id(db, user_id)

#         if not instructor:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Instructor not found.",
#             )

#         return await InstructorRepository.update(db, instructor, data)

#     @staticmethod
#     async def delete_instructor(
#         db: AsyncSession,
#         user_id: int,
#     ):
#         instructor = await InstructorRepository.get_by_id(db, user_id)

#         if not instructor:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Instructor not found.",
#             )

#         await InstructorRepository.delete(db, instructor)

#         return {"message": "Instructor deleted successfully."}