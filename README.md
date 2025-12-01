# cashlog - 轻量化本地记账/待办CLI工具

一款基于Python 3.10+的轻量化本地记账/待办CLI工具，采用分层架构设计，代码规范严格，易于扩展。

## 功能特性

### 收支管理
- 新增收支记录：支持录入金额、分类、标签、备注、时间
- 查询收支记录：支持按月度、分类、标签、收支类型筛选
- 月度收支报表：生成指定月度的收支汇总和分类占比报表，支持文本和Markdown格式

### 待办管理
- 新增待办事项：支持录入内容、分类、标签、截止时间
- 更新待办状态：支持按ID修改待办状态（todo/doing/done）
- 查询待办事项：支持按状态、分类、截止时间筛选
- 删除待办事项：支持按ID删除待办事项

## 技术栈

- **Python 3.10+**：编程语言
- **SQLAlchemy**：ORM框架，操作SQLite数据库
- **Click**：CLI框架，构建命令行界面
- **Tabulate**：表格格式化输出
- **Python-dateutil**：日期时间处理
- **Pytest**：单元测试框架

## 安装与运行

### 环境要求
- Python 3.10+
- uv CLI工具（用于依赖管理）

### 安装步骤

1. **安装uv CLI工具**（如果尚未安装）：
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **安装项目依赖**：
   ```bash
   uv sync
   ```

### 运行工具

```bash
uv run python main.py --help
```

## 命令示例

### 收支管理

#### 新增收入记录
```bash
uv run python main.py transaction add -a 1000 -c 工资 -t 收入,工资 -r 2024年1月工资
```

#### 新增支出记录
```bash
uv run python main.py transaction add -a -500 -c 餐饮 -t 支出,餐饮 -r 午餐
```

#### 查询所有收支记录
```bash
uv run python main.py transaction list
```

#### 查询2024年1月的收支记录
```bash
uv run python main.py transaction list -m 1 -y 2024
```

#### 查询收入记录
```bash
uv run python main.py transaction list -ty income
```

#### 生成2024年1月的收支报表
```bash
uv run python main.py transaction summary -m 1 -y 2024
```

#### 生成Markdown格式的收支报表
```bash
uv run python main.py transaction summary -m 1 -y 2024 -f markdown
```

### 待办管理

#### 新增待办事项
```bash
uv run python main.py todo add -c 完成项目报告 -ca 工作 -d 2024-01-15 18:00:00
```

#### 更新待办状态为doing
```bash
uv run python main.py todo update -i 1 -s doing
```

#### 更新待办状态为done
```bash
uv run python main.py todo update -i 1 -s done
```

#### 查询所有待办事项
```bash
uv run python main.py todo list
```

#### 查询状态为todo的待办事项
```bash
uv run python main.py todo list -s todo
```

#### 查询分类为工作的待办事项
```bash
uv run python main.py todo list -ca 工作
```

#### 删除待办事项
```bash
uv run python main.py todo delete -i 1
```

## 测试

### 运行单元测试
```bash
uv run pytest tests/ -v
```

### 运行测试并查看覆盖率
```bash
uv run pytest tests/ -v --cov=cashlog --cov-report=term-missing
```

## 项目结构

```
cashlog03/
├── cashlog/                # 项目主目录
│   ├── __init__.py        # 包初始化文件
│   ├── data/              # 数据模型层
│   │   ├── __init__.py
│   │   ├── models.py      # 数据库模型定义
│   │   └── database.py    # 数据库连接和初始化
│   ├── service/           # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── transaction_service.py  # 收支管理业务逻辑
│   │   └── todo_service.py         # 待办管理业务逻辑
│   └── cli/               # CLI接口层
│       ├── __init__.py
│       ├── main.py        # 主CLI入口
│       ├── transaction_cli.py  # 收支管理CLI命令
│       └── todo_cli.py         # 待办管理CLI命令
├── tests/                 # 单元测试目录
│   ├── __init__.py
│   ├── test_database.py       # 数据库测试
│   ├── test_transaction_service.py  # 收支管理业务逻辑测试
│   └── test_todo_service.py         # 待办管理业务逻辑测试
├── main.py                # 项目入口文件
├── pyproject.toml         # 项目配置文件
└── README.md              # 项目说明文档
```

## 扩展开发

### 添加新功能模块

1. 在`cashlog/data/models.py`中定义新的数据模型
2. 在`cashlog/service/`中创建新的业务逻辑模块
3. 在`cashlog/cli/`中创建新的CLI命令模块
4. 在`cashlog/cli/main.py`中注册新的命令组

### 运行新功能

```bash
uv run python main.py <new-command> --help
```

## 许可证

MIT License
