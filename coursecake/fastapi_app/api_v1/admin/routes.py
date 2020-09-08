# contains all routes for the courses endpoint
from typing import List, Optional

from fastapi import (
    Depends,
    APIRouter,
    BackgroundTasks,
    status,
    HTTPException,
    Query,
    Request,
)
from sqlalchemy.orm import Session

from ....database import crud, models, sql, uploads
from ...limiter import limiter
from .. import schemas
from . import utils

router = APIRouter()

# dependency
def get_db():
    db = sql.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/update/all")
@limiter.limit("2/minute")
async def update_all(
    request: Request,
    token: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    term_id: str = Query("2020-fall"),
    testing: bool = Query(False),
):

    if not utils.verifyAdminToken(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token"
        )

    background_tasks.add_task(uploads.update_all, db, term_id, testing)

    return {
        "message": "initiated updates for all database information via scrapers. this will take a few minutes."
    }
