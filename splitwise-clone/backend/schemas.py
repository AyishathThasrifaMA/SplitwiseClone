from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Enums
class SplitType(str, Enum):
    equal = "equal"
    percentage = "percentage"

# User Schemas
class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Group Schemas
class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    user_ids: List[int]

class Group(GroupBase):
    id: int
    users: List[User] = []

    class Config:
        orm_mode = True

# Expense Splits
class Split(BaseModel):
    user_id: int
    percentage: Optional[float] = None  # Required for percentage split

# Expense Schemas
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    paid_by: int
    split_type: SplitType
    splits: List[Split]

class Expense(BaseModel):
    id: int
    description: str
    amount: float
    paid_by: int
    split_type: SplitType
    group_id: int

    class Config:
        orm_mode = True

# Balance Schema
class BalanceResponse(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: float
