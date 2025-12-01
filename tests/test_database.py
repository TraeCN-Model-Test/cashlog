import pytest
import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from cashlog.data.models import Base, Transaction, Todo, TransactionType, TodoStatus
from cashlog.data.database import Database
from datetime import datetime
import tempfile

@pytest.fixture
def temp_db():
    """创建临时数据库"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db_path = f.name
    
    # 创建数据库引擎
    engine = create_engine(f'sqlite:///{temp_db_path}')
    # 创建表
    Base.metadata.create_all(bind=engine)
    # 创建会话工厂
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield SessionLocal
    
    # 清理
    os.unlink(temp_db_path)

def test_database_initialization():
    """测试数据库初始化"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db_path = f.name
    
    try:
        # 创建数据库实例
        db = Database(db_path=temp_db_path)
        # 检查表是否创建
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert 'transactions' in tables
        assert 'todos' in tables
    finally:
        os.unlink(temp_db_path)

def test_transaction_model(temp_db):
    """测试收支记录模型"""
    session = temp_db()
    
    # 创建测试数据
    transaction = Transaction(
        amount=100.0,
        category='工资',
        tags='收入,工资',
        remark='2024年1月工资',
        transaction_time=datetime(2024, 1, 1, 10, 0, 0)
    )
    
    # 添加到数据库
    session.add(transaction)
    session.commit()
    
    # 查询数据
    retrieved = session.query(Transaction).filter_by(id=transaction.id).first()
    
    # 验证数据
    assert retrieved is not None
    assert retrieved.amount == 100.0
    assert retrieved.category == '工资'
    assert retrieved.tags == '收入,工资'
    assert retrieved.remark == '2024年1月工资'
    assert retrieved.transaction_time == datetime(2024, 1, 1, 10, 0, 0)
    assert retrieved.type == TransactionType.INCOME
    
    session.close()

def test_todo_model(temp_db):
    """测试待办事项模型"""
    session = temp_db()
    
    # 创建测试数据
    todo = Todo(
        content='完成项目报告',
        category='工作',
        tags='报告,工作',
        deadline=datetime(2024, 1, 15, 18, 0, 0),
        status=TodoStatus.DOING
    )
    
    # 添加到数据库
    session.add(todo)
    session.commit()
    
    # 查询数据
    retrieved = session.query(Todo).filter_by(id=todo.id).first()
    
    # 验证数据
    assert retrieved is not None
    assert retrieved.content == '完成项目报告'
    assert retrieved.category == '工作'
    assert retrieved.tags == '报告,工作'
    assert retrieved.deadline == datetime(2024, 1, 15, 18, 0, 0)
    assert retrieved.status == TodoStatus.DOING
    
    session.close()
