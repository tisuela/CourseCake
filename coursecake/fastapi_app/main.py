from fastapi import FastAPI

from ..database import crud, models, sql

from .api_v1.courses import routes as v1_courses_routes
from .api_v1.admin import routes as v1_admin_routes

models.Base.metadata.create_all(bind=sql.engine)


tags_metadata= [
    {
        "name": "courses",
        "description": "Find all course information here",
        "externalDocs": {
            "description"; "Courses external docs"
        }
    }
]


app = FastAPI(
        title = "CourseCake"
        version="v1.0-beta"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    v1_courses_routes.router,
    prefix="/api/v1/courses",
    tags=["courses"])


app.include_router(
    v1_admin_routes.router,
    prefix="/api/v1/admin",
    tags=["admin"])
