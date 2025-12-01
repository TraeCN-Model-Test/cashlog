from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class TransactionType(enum.Enum):
    """收支类型枚举"""
    INCOME = "income"
    EXPENSE = "expense"

class TodoStatus(enum.Enum):
    """待办状态枚举"""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Transaction(Base):
    """收支记录模型"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(String(200), nullable=True)
    remark = Column(String(500), nullable=True)
    transaction_time = Column(DateTime, nullable=False, default=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    @property
    def type(self):
        """根据金额判断收支类型"""
        return TransactionType.INCOME if self.amount > 0 else TransactionType.EXPENSE

class Todo(Base):
    """待办事项模型"""
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(String(200), nullable=True)
    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(TodoStatus), nullable=False, default=TodoStatus.TODO)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
