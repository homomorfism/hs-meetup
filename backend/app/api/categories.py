from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Category
from ..schemas.category import Category as CategorySchema

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategorySchema])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories
