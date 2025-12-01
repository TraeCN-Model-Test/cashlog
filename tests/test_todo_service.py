import pytest
import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cashlog.service.todo_service import TodoService
from cashlog.data.models import Todo, TodoStatus
from datetime import datetime
from tests.test_database import temp_db

def test_add_todo(temp_db):
    """测试新增待办事项"""
    session = temp_db()
    service = TodoService(session)
    
    # 测试正常新增待办事项
    todo = service.add_todo(
        content='完成项目报告',
        category='工作',
        tags='报告,工作',
        deadline=datetime(2024, 1, 15, 18, 0, 0)
    )
    
    assert todo is not None
    assert todo.id is not None
    assert todo.content == '完成项目报告'
    assert todo.category == '工作'
    assert todo.status == TodoStatus.TODO
    
    session.close()

def test_update_todo_status(temp_db):
    """测试更新待办事项状态"""
    session = temp_db()
    service = TodoService(session)
    
    # 添加测试数据
    todo = service.add_todo('完成项目报告', '工作')
    
    # 测试更新状态为doing
    updated_todo = service.update_todo_status(todo.id, TodoStatus.DOING)
    assert updated_todo is not None
    assert updated_todo.status == TodoStatus.DOING
    
    # 测试更新状态为done
    updated_todo2 = service.update_todo_status(todo.id, TodoStatus.DONE)
    assert updated_todo2 is not None
    assert updated_todo2.status == TodoStatus.DONE
    
    # 测试更新不存在的待办事项
    updated_todo3 = service.update_todo_status(999, TodoStatus.DOING)
    assert updated_todo3 is None
    
    session.close()

def test_get_todos(temp_db):
    """测试查询待办事项"""
    session = temp_db()
    service = TodoService(session)
    
    # 添加测试数据
    service.add_todo('完成项目报告', '工作', deadline=datetime(2024, 1, 15, 18, 0, 0))
    todo2 = service.add_todo('购买生活用品', '生活')
    service.update_todo_status(todo2.id, TodoStatus.DOING)
    todo3 = service.add_todo('学习Python', '学习', deadline=datetime(2024, 1, 20, 20, 0, 0))
    service.update_todo_status(todo3.id, TodoStatus.DONE)
    service.add_todo('锻炼身体', '健康')
    
    # 测试查询所有待办事项
    all_todos = service.get_todos()
    assert len(all_todos) == 4
    
    # 测试按状态查询
    todo_todos = service.get_todos(status=TodoStatus.TODO)
    assert len(todo_todos) == 2
    
    doing_todos = service.get_todos(status=TodoStatus.DOING)
    assert len(doing_todos) == 1
    
    done_todos = service.get_todos(status=TodoStatus.DONE)
    assert len(done_todos) == 1
    
    # 测试按分类查询
    work_todos = service.get_todos(category='工作')
    assert len(work_todos) == 1
    
    # 测试按截止时间查询
    before_deadline = datetime(2024, 1, 25, 0, 0, 0)
    deadline_todos = service.get_todos(deadline_before=before_deadline)
    assert len(deadline_todos) == 2
    
    session.close()

def test_delete_todo(temp_db):
    """测试删除待办事项"""
    session = temp_db()
    service = TodoService(session)
    
    # 添加测试数据
    todo = service.add_todo('完成项目报告', '工作')
    
    # 测试删除存在的待办事项
    success = service.delete_todo(todo.id)
    assert success is True
    
    # 测试删除不存在的待办事项
    success2 = service.delete_todo(999)
    assert success2 is False
    
    # 验证删除结果
    todos = service.get_todos()
    assert len(todos) == 0
    
    session.close()
