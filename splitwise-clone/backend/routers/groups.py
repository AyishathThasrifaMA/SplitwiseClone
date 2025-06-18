from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

@router.post("/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, group)

@router.get("/{group_id}", response_model=schemas.Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.get("/{group_id}/balances")
def get_group_balances(group_id: int, db: Session = Depends(get_db)):
    balances = crud.get_balances_for_group(db, group_id)
    if balances is None:
        raise HTTPException(status_code=404, detail="Group not found or no balances")
    return balances
