from fastapi import FastAPI
from starlette.requests import Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from ..database import crud, models, sql
from .api_v1.courses import routes as v1_courses_routes
from .api_v1.classes import routes as v1_classes_routes
from .api_v1.admin import routes as v1_admin_routes
from .limiter import limiter


models.Base.metadata.create_all(bind=sql.engine)

tags_metadata= [
    {
        "name": "courses",
        "description": "Find all course information here",
        "externalDocs": {
            "description": "Courses external docs",
            "url": "https://docs.coursecake.tisuela.com/RESTful-API"
        }
    }
]

app = FastAPI(
        title = "CourseCake",
        version="v1.0-beta",
        openapi_tags=tags_metadata,
        redoc_url = "/",
        docs_url = "/api/v1"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/hello")
async def hello(request: Request):
    return {"message": "Hello World"}

app.include_router(
    v1_courses_routes.router,
    prefix="/api/v1/courses",
    tags=["courses"])

app.include_router(
    v1_classes_routes.router,
    prefix="/api/v1/classes",
    tags=["classes"])

app.include_router(
    v1_admin_routes.router,
    prefix="/api/v1/admin",
    tags=["admin"])
