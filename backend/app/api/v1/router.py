from fastapi import APIRouter

from app.api.v1 import admin, questions, quiz, user

api_router = APIRouter()

api_router.include_router(questions.router, tags=["questions"])
api_router.include_router(quiz.router, tags=["quiz"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(admin.router, tags=["admin"])
