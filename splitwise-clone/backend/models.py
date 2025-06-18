from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

# Enum for Split Type
class SplitType(str, enum.Enum):
    equal = "equal"
    percentage = "percentage"

# Many-to-Many: Group <-> User
group_user = Table(
    'group_user',
    Base.metadata,
    Column('group_id', ForeignKey('groups.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)

# Group model
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("User", secondary=group_user, back_populates="groups")
    expenses = relationship("Expense", back_populates="group")

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    groups = relationship("Group", secondary=group_user, back_populates="users")

# Expense model
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    paid_by = Column(Integer, ForeignKey("users.id"))
    split_type = Column(Enum(SplitType))
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="expenses")

# Balance model
class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)

    @staticmethod
    def update_balance(db, group_id, payer_id, receiver_id, amount):
        existing = db.query(Balance).filter_by(
            group_id=group_id,
            from_user_id=receiver_id,
            to_user_id=payer_id
        ).first()

        if existing:
            existing.amount -= amount
            if existing.amount < 0:
                existing.from_user_id, existing.to_user_id = existing.to_user_id, existing.from_user_id
                existing.amount = abs(existing.amount)
        else:
            new_balance = Balance(
                group_id=group_id,
                from_user_id=payer_id,
                to_user_id=receiver_id,
                amount=amount
            )
            db.add(new_balance)
        db.commit()
