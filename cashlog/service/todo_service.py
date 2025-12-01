from sqlalchemy.orm import Session
from datetime import datetime
from ..data.models import Todo, TodoStatus
from typing import List, Optional

class TodoService:
    """待办事项业务逻辑层"""
    
    def __init__(self, db_session: Session):
        """初始化业务逻辑层
        
        Args:
            db_session (Session): 数据库会话对象
        """
        self.db_session = db_session
    
    def add_todo(self, content: str, category: str, tags: Optional[str] = None, 
                deadline: Optional[datetime] = None) -> Todo:
        """新增待办事项
        
        Args:
            content (str): 待办内容
            category (str): 分类
            tags (Optional[str], optional): 标签，多个标签用逗号分隔. Defaults to None.
            deadline (Optional[datetime], optional): 截止时间. Defaults to None.
        
        Returns:
            Todo: 新增的待办事项对象
        """
        todo = Todo(
            content=content,
            category=category,
            tags=tags,
            deadline=deadline
        )
        
        self.db_session.add(todo)
        self.db_session.commit()
        self.db_session.refresh(todo)
        
        return todo
    
    def update_todo_status(self, todo_id: int, status: TodoStatus) -> Optional[Todo]:
        """更新待办事项状态
        
        Args:
            todo_id (int): 待办事项ID
            status (TodoStatus): 新状态
        
        Returns:
            Optional[Todo]: 更新后的待办事项对象，若不存在则返回None
        """
        todo = self.db_session.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            todo.status = status
            self.db_session.commit()
            self.db_session.refresh(todo)
        return todo
    
    def get_todos(self, status: Optional[TodoStatus] = None, category: Optional[str] = None, 
                 deadline_before: Optional[datetime] = None) -> List[Todo]:
        """查询待办事项
        
        Args:
            status (Optional[TodoStatus], optional): 状态. Defaults to None.
            category (Optional[str], optional): 分类. Defaults to None.
            deadline_before (Optional[datetime], optional): 截止时间之前. Defaults to None.
        
        Returns:
            List[Todo]: 待办事项列表
        """
        query = self.db_session.query(Todo)
        
        # 按状态筛选
        if status is not None:
            query = query.filter(Todo.status == status)
        
        # 按分类筛选
        if category is not None:
            query = query.filter(Todo.category == category)
        
        # 按截止时间筛选
        if deadline_before is not None:
            query = query.filter(Todo.deadline <= deadline_before)
        
        # 按创建时间降序排列
        return query.order_by(Todo.created_at.desc()).all()
    
    def delete_todo(self, todo_id: int) -> bool:
        """删除待办事项
        
        Args:
            todo_id (int): 待办事项ID
        
        Returns:
            bool: 删除成功返回True，否则返回False
        """
        todo = self.db_session.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            self.db_session.delete(todo)
            self.db_session.commit()
            return True
        return False
