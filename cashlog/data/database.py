from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
from .models import Base

class Database:
    """数据库连接和初始化类"""
    
    def __init__(self, db_path=None):
        """初始化数据库连接
        
        Args:
            db_path (str, optional): 数据库文件路径. 默认None，将使用用户主目录下的cashlog.db
        """
        if db_path is None:
            # 获取用户主目录
            home_dir = Path.home()
            # 创建cashlog目录
            cashlog_dir = home_dir / ".cashlog"
            cashlog_dir.mkdir(exist_ok=True)
            # 数据库文件路径
            db_path = str(cashlog_dir / "cashlog.db")
        
        # 创建SQLite引擎
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        # 创建会话工厂
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # 初始化数据库表
        self.init_db()
    
    def init_db(self):
        """初始化数据库表"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """获取数据库会话
        
        Returns:
            Session: 数据库会话对象
        """
        return self.SessionLocal()

# 创建全局数据库实例
db = Database()
