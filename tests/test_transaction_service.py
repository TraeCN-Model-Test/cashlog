import pytest
import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cashlog.service.transaction_service import TransactionService
from cashlog.data.models import Transaction, TransactionType
from datetime import datetime
from tests.test_database import temp_db

def test_add_transaction(temp_db):
    """测试新增收支记录"""
    session = temp_db()
    service = TransactionService(session)
    
    # 测试正常新增收入
    transaction = service.add_transaction(
        amount=1000.0,
        category='工资',
        tags='收入,工资',
        remark='2024年1月工资',
        transaction_time=datetime(2024, 1, 1, 10, 0, 0)
    )
    
    assert transaction is not None
    assert transaction.id is not None
    assert transaction.amount == 1000.0
    assert transaction.category == '工资'
    assert transaction.type == TransactionType.INCOME
    
    # 测试正常新增支出
    transaction2 = service.add_transaction(
        amount=-500.0,
        category='餐饮',
        tags='支出,餐饮',
        remark='午餐',
        transaction_time=datetime(2024, 1, 2, 12, 0, 0)
    )
    
    assert transaction2 is not None
    assert transaction2.amount == -500.0
    assert transaction2.category == '餐饮'
    assert transaction2.type == TransactionType.EXPENSE
    
    session.close()

def test_get_transactions(temp_db):
    """测试查询收支记录"""
    session = temp_db()
    service = TransactionService(session)
    
    # 添加测试数据
    service.add_transaction(1000.0, '工资', '收入,工资', '2024年1月工资', datetime(2024, 1, 1, 10, 0, 0))
    service.add_transaction(-500.0, '餐饮', '支出,餐饮', '午餐', datetime(2024, 1, 2, 12, 0, 0))
    service.add_transaction(-200.0, '交通', '支出,交通', '地铁费', datetime(2024, 1, 3, 8, 0, 0))
    service.add_transaction(500.0, '奖金', '收入,奖金', '季度奖金', datetime(2024, 2, 1, 15, 0, 0))
    
    # 测试查询所有记录
    all_transactions = service.get_transactions()
    assert len(all_transactions) == 4
    
    # 测试按月份查询
    jan_transactions = service.get_transactions(month=1, year=2024)
    assert len(jan_transactions) == 3
    
    # 测试按分类查询
    food_transactions = service.get_transactions(category='餐饮')
    assert len(food_transactions) == 1
    assert food_transactions[0].amount == -500.0
    
    # 测试按收支类型查询
    income_transactions = service.get_transactions(transaction_type=TransactionType.INCOME)
    assert len(income_transactions) == 2
    
    expense_transactions = service.get_transactions(transaction_type=TransactionType.EXPENSE)
    assert len(expense_transactions) == 2
    
    session.close()

def test_get_monthly_summary(temp_db):
    """测试获取月度收支汇总"""
    session = temp_db()
    service = TransactionService(session)
    
    # 添加测试数据
    service.add_transaction(1000.0, '工资', '收入,工资', '2024年1月工资', datetime(2024, 1, 1, 10, 0, 0))
    service.add_transaction(-500.0, '餐饮', '支出,餐饮', '午餐', datetime(2024, 1, 2, 12, 0, 0))
    service.add_transaction(-200.0, '交通', '支出,交通', '地铁费', datetime(2024, 1, 3, 8, 0, 0))
    service.add_transaction(500.0, '奖金', '收入,奖金', '季度奖金', datetime(2024, 2, 1, 15, 0, 0))
    
    # 测试2024年1月汇总
    summary = service.get_monthly_summary(month=1, year=2024)
    assert summary['total_income'] == 1000.0
    assert summary['total_expense'] == 700.0
    assert summary['balance'] == 300.0
    assert summary['transaction_count'] == 3
    assert '工资' in summary['category_stats']
    assert '餐饮' in summary['category_stats']
    assert '交通' in summary['category_stats']
    assert summary['category_stats']['工资'] == 1000.0
    assert summary['category_stats']['餐饮'] == 500.0
    assert summary['category_stats']['交通'] == 200.0
    
    # 测试没有交易记录的月份
    summary2 = service.get_monthly_summary(month=3, year=2024)
    assert summary2['total_income'] == 0.0
    assert summary2['total_expense'] == 0.0
    assert summary2['balance'] == 0.0
    assert summary2['transaction_count'] == 0
    
    session.close()
