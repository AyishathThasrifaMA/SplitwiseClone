from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db

router = APIRouter(
    prefix="/groups/{group_id}/expenses",
    tags=["Expenses"]
)

@router.post("/", response_model=schemas.Expense)
def add_expense(group_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    try:
        return crud.add_expense_to_group(db, group_id, expense)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
