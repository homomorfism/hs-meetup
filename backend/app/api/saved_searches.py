from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import SavedSearch, User
from ..schemas.saved_search import SavedSearch as SavedSearchSchema, SavedSearchCreate, SavedSearchUpdate
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/saved-searches", tags=["Saved Searches"])


@router.get("/", response_model=List[SavedSearchSchema])
def list_saved_searches(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all saved searches for the current user"""
    searches = db.query(SavedSearch).filter(SavedSearch.user_id == current_user.id).order_by(SavedSearch.created_at.desc()).all()
    return searches


@router.get("/{search_id}", response_model=SavedSearchSchema)
def get_saved_search(
    search_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific saved search"""
    search = db.query(SavedSearch).filter(
        SavedSearch.id == search_id,
        SavedSearch.user_id == current_user.id
    ).first()

    if not search:
        raise HTTPException(status_code=404, detail="Saved search not found")

    return search


@router.post("/", response_model=SavedSearchSchema, status_code=201)
def create_saved_search(
    search: SavedSearchCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new saved search"""
    db_search = SavedSearch(**search.model_dump(), user_id=current_user.id)
    db.add(db_search)
    db.commit()
    db.refresh(db_search)
    return db_search


@router.put("/{search_id}", response_model=SavedSearchSchema)
def update_saved_search(
    search_id: int,
    search_update: SavedSearchUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a saved search"""
    db_search = db.query(SavedSearch).filter(
        SavedSearch.id == search_id,
        SavedSearch.user_id == current_user.id
    ).first()

    if not db_search:
        raise HTTPException(status_code=404, detail="Saved search not found")

    update_data = search_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_search, field, value)

    db.commit()
    db.refresh(db_search)
    return db_search


@router.delete("/{search_id}")
def delete_saved_search(
    search_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a saved search"""
    db_search = db.query(SavedSearch).filter(
        SavedSearch.id == search_id,
        SavedSearch.user_id == current_user.id
    ).first()

    if not db_search:
        raise HTTPException(status_code=404, detail="Saved search not found")

    db.delete(db_search)
    db.commit()

    return {"message": "Saved search deleted successfully"}
