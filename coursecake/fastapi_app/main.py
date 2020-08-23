from fastapi import FastAPI

from .api_v1.courses import routes as v1_courses_routes
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    v1_courses_routes.router,
    prefix="/api/v1/courses",
    tags=["courses"])
