from sqlalchemy.orm import Session
from models import User, Group, Expense, Balance, SplitType
import schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = Group(name=group.name)
    db_group.users = db.query(User).filter(User.id.in_(group.user_ids)).all()
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()

def add_expense(db: Session, group_id: int, expense: schemas.ExpenseCreate):
    db_expense = Expense(
        description=expense.description,
        amount=expense.amount,
        paid_by=expense.paid_by,
        split_type=expense.split_type,
        group_id=group_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return None

    total_amount = expense.amount
    if expense.split_type == SplitType.equal:
        per_user = total_amount / len(group.users)
        for user in group.users:
            if user.id != expense.paid_by:
                Balance.update_balance(db, group_id, expense.paid_by, user.id, per_user)
    elif expense.split_type == SplitType.percentage:
        for split in expense.splits:
            if split.user_id != expense.paid_by:
                owed_amount = total_amount * (split.percentage / 100)
                Balance.update_balance(db, group_id, expense.paid_by, split.user_id, owed_amount)
    return db_expense

def get_balances_for_group(db: Session, group_id: int):
    return db.query(Balance).filter(Balance.group_id == group_id).all()

def get_balances_for_user(db: Session, user_id: int):
    return db.query(Balance).filter(
        (Balance.from_user_id == user_id) | (Balance.to_user_id == user_id)
    ).all()
