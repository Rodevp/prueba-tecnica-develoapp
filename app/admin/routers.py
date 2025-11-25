from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import session_local
from app.core.utilitys import require_permission
from app.admin.services import get_stats

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/dashboard/stats",
    dependencies=[Depends(require_permission("dashboard:view"))]
)
def route_dashboard_stats(
    db: Session = Depends(get_db)
):
    return get_stats(db)
