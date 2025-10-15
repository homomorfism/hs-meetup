from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import SearchHistory, User
from ..schemas.search_history import SearchHistory as SearchHistorySchema, SearchHistoryCreate
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/search-history", tags=["Search History"])


@router.get("/", response_model=List[SearchHistorySchema])
def list_search_history(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get recent search history for the current user"""
    history = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id
    ).order_by(SearchHistory.searched_at.desc()).limit(limit).all()
    return history


@router.post("/", response_model=SearchHistorySchema, status_code=201)
def create_search_history(
    search: SearchHistoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Record a new search in history"""
    # Check if this exact search already exists recently (within last search)
    # If it does, we can update its timestamp instead of creating duplicate
    recent_search = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id,
        SearchHistory.keyword == search.keyword,
        SearchHistory.location == search.location,
        SearchHistory.category == search.category,
        SearchHistory.is_online == search.is_online,
        SearchHistory.price == search.price
    ).order_by(SearchHistory.searched_at.desc()).first()

    if recent_search:
        # Update the timestamp of existing search
        from datetime import datetime
        recent_search.searched_at = datetime.utcnow()
        db.commit()
        db.refresh(recent_search)
        return recent_search

    # Create new search history entry
    db_search = SearchHistory(**search.model_dump(), user_id=current_user.id)
    db.add(db_search)
    db.commit()
    db.refresh(db_search)

    # Keep only last 50 searches per user to prevent unlimited growth
    all_searches = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id
    ).order_by(SearchHistory.searched_at.desc()).all()

    if len(all_searches) > 50:
        for old_search in all_searches[50:]:
            db.delete(old_search)
        db.commit()

    return db_search


@router.delete("/{search_id}")
def delete_search_history(
    search_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a search from history"""
    db_search = db.query(SearchHistory).filter(
        SearchHistory.id == search_id,
        SearchHistory.user_id == current_user.id
    ).first()

    if not db_search:
        raise HTTPException(status_code=404, detail="Search history not found")

    db.delete(db_search)
    db.commit()

    return {"message": "Search history deleted successfully"}


@router.delete("/")
def clear_search_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear all search history for the current user"""
    db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id
    ).delete()
    db.commit()

    return {"message": "Search history cleared successfully"}
