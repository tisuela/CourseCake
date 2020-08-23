# contains all routes for the courses endpoint
from fastapi import APIRouter

router = APIRouter()

@router.get("/all/{university}")
async def all_courses(university: str):
    return {"all": "courses"}
