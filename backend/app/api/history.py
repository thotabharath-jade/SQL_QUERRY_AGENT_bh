from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.query_history import QueryHistoryResponse, QueryHistoryCreate

router = APIRouter(prefix="/history", tags=["Query History"])


@router.get("/", response_model=List[QueryHistoryResponse])
async def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.query_history import QueryHistory
    history = db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id
    ).order_by(QueryHistory.created_at.desc()).all()
    return history


@router.get("/bookmarked", response_model=List[QueryHistoryResponse])
async def get_bookmarked(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.query_history import QueryHistory
    history = db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id,
        QueryHistory.is_bookmarked == True
    ).order_by(QueryHistory.created_at.desc()).all()
    return history


@router.post("/{history_id}/bookmark", response_model=QueryHistoryResponse)
async def toggle_bookmark(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.query_history import QueryHistory
    history_item = db.query(QueryHistory).filter(
        QueryHistory.id == history_id,
        QueryHistory.user_id == current_user.id
    ).first()
    
    if not history_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Query history not found"
        )
    
    history_item.is_bookmarked = not history_item.is_bookmarked
    db.commit()
    db.refresh(history_item)
    return history_item
