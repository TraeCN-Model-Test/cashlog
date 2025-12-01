from sqlalchemy.orm import Session
from datetime import datetime, date
from ..data.models import Transaction, TransactionType
from typing import List, Optional

class TransactionService:
    """收支记录业务逻辑层"""
    
    def __init__(self, db_session: Session):
        """初始化业务逻辑层
        
        Args:
            db_session (Session): 数据库会话对象
        """
        self.db_session = db_session
    
    def add_transaction(self, amount: float, category: str, tags: Optional[str] = None, 
                      remark: Optional[str] = None, transaction_time: Optional[datetime] = None) -> Transaction:
        """新增收支记录
        
        Args:
            amount (float): 金额，正数为收入，负数为支出
            category (str): 分类
            tags (Optional[str], optional): 标签，多个标签用逗号分隔. Defaults to None.
            remark (Optional[str], optional): 备注. Defaults to None.
            transaction_time (Optional[datetime], optional): 交易时间. Defaults to None.
        
        Returns:
            Transaction: 新增的收支记录对象
        """
        if transaction_time is None:
            transaction_time = datetime.now()
        
        transaction = Transaction(
            amount=amount,
            category=category,
            tags=tags,
            remark=remark,
            transaction_time=transaction_time
        )
        
        self.db_session.add(transaction)
        self.db_session.commit()
        self.db_session.refresh(transaction)
        
        return transaction
    
    def get_transactions(self, month: Optional[int] = None, year: Optional[int] = None, 
                       category: Optional[str] = None, tags: Optional[str] = None, 
                       transaction_type: Optional[TransactionType] = None) -> List[Transaction]:
        """查询收支记录
        
        Args:
            month (Optional[int], optional): 月份 (1-12). Defaults to None.
            year (Optional[int], optional): 年份. Defaults to None.
            category (Optional[str], optional): 分类. Defaults to None.
            tags (Optional[str], optional): 标签. Defaults to None.
            transaction_type (Optional[TransactionType], optional): 收支类型. Defaults to None.
        
        Returns:
            List[Transaction]: 收支记录列表
        """
        query = self.db_session.query(Transaction)
        
        # 按月份和年份筛选
        if month is not None and year is not None:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            query = query.filter(Transaction.transaction_time >= start_date, 
                               Transaction.transaction_time < end_date)
        
        # 按分类筛选
        if category is not None:
            query = query.filter(Transaction.category == category)
        
        # 按标签筛选
        if tags is not None:
            query = query.filter(Transaction.tags.contains(tags))
        
        # 按收支类型筛选
        if transaction_type is not None:
            if transaction_type == TransactionType.INCOME:
                query = query.filter(Transaction.amount > 0)
            else:
                query = query.filter(Transaction.amount < 0)
        
        # 按交易时间降序排列
        return query.order_by(Transaction.transaction_time.desc()).all()
    
    def get_monthly_summary(self, month: int, year: int) -> dict:
        """获取月度收支汇总
        
        Args:
            month (int): 月份 (1-12)
            year (int): 年份
        
        Returns:
            dict: 月度收支汇总数据
        """
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # 获取当月所有交易
        transactions = self.db_session.query(Transaction).filter(
            Transaction.transaction_time >= start_date, 
            Transaction.transaction_time < end_date
        ).all()
        
        # 计算总收入、总支出
        total_income = sum(t.amount for t in transactions if t.amount > 0)
        total_expense = abs(sum(t.amount for t in transactions if t.amount < 0))
        balance = total_income - total_expense
        
        # 计算分类占比
        category_stats = {}
        for t in transactions:
            cat = t.category
            amount = abs(t.amount)
            if cat not in category_stats:
                category_stats[cat] = 0
            category_stats[cat] += amount
        
        # 计算占比百分比
        total_amount = total_income + total_expense
        category_percentage = {}
        for cat, amount in category_stats.items():
            if total_amount > 0:
                category_percentage[cat] = round((amount / total_amount) * 100, 2)
            else:
                category_percentage[cat] = 0.0
        
        return {
            "month": month,
            "year": year,
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "transaction_count": len(transactions),
            "category_stats": category_stats,
            "category_percentage": category_percentage
        }
