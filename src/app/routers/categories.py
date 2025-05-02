from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from src.db import get_session
from src.models import Category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: Category,
    session: Session = Depends(get_session),
):
    exists = session.exec(
        select(Category).where(Category.name == category.name)
    ).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name must be unique."
        )
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/", response_model=List[Category])
def list_categories(session: Session = Depends(get_session)):
    cats = session.exec(select(Category)).all()
    # format monthly_budget as dollars
    for c in cats:
        c.monthly_budget = f"${c.monthly_budget / 100:,.2f}"
    return cats


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    cat = session.get(Category, category_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found."
        )
    session.delete(cat)
    session.commit()
    return
