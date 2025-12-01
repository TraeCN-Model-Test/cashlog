import click
from tabulate import tabulate
from datetime import datetime
from cashlog.data.database import db
from cashlog.service.todo_service import TodoService
from cashlog.data.models import TodoStatus

def validate_date(ctx, param, value):
    """验证日期格式是否正确"""
    if value is None:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise click.BadParameter('日期格式需为 YYYY-MM-DD HH:MM:SS')

def validate_todo_id(ctx, param, value):
    """验证待办事项ID是否为正整数"""
    try:
        todo_id = int(value)
        if todo_id <= 0:
            raise ValueError
        return todo_id
    except ValueError:
        raise click.BadParameter('待办事项ID需为正整数')

@click.group(name='todo', help='待办事项管理命令')
def todo_cli():
    """待办事项管理命令组"""
    pass

@todo_cli.command(name='add', help='新增待办事项')
@click.option('--content', '-c', required=True, help='待办内容')
@click.option('--category', '-ca', help='分类')
@click.option('--tags', '-t', help='标签，多个标签用逗号分隔')
@click.option('--deadline', '-d', callback=validate_date, help='截止时间，格式：YYYY-MM-DD HH:MM:SS')
def add_todo(content, category, tags, deadline):
    """新增待办事项命令"""
    try:
        session = db.get_session()
        service = TodoService(session)
        todo = service.add_todo(content, category, tags, deadline)
        click.echo(f'待办事项新增成功！ID: {todo.id}')
    except Exception as e:
        click.echo(f'待办事项新增失败：{str(e)}', err=True)

@todo_cli.command(name='update', help='更新待办事项状态')
@click.option('--id', '-i', required=True, callback=validate_todo_id, help='待办事项ID')
@click.option('--status', '-s', required=True, type=click.Choice(['todo', 'doing', 'done']), help='新状态')
def update_todo(id, status):
    """更新待办事项状态命令"""
    try:
        session = db.get_session()
        service = TodoService(session)
        todo_status = TodoStatus(status)
        todo = service.update_todo_status(id, todo_status)
        if todo:
            click.echo(f'待办事项状态更新成功！ID: {todo.id}，新状态: {todo.status.value}')
        else:
            click.echo(f'待办事项不存在：ID {id}', err=True)
    except Exception as e:
        click.echo(f'更新待办事项状态失败：{str(e)}', err=True)

@todo_cli.command(name='list', help='查询待办事项')
@click.option('--status', '-s', type=click.Choice(['todo', 'doing', 'done']), help='状态')
@click.option('--category', '-ca', help='分类')
@click.option('--deadline-before', '-db', callback=validate_date, help='截止时间之前，格式：YYYY-MM-DD HH:MM:SS')
def list_todos(status, category, deadline_before):
    """查询待办事项命令"""
    try:
        session = db.get_session()
        service = TodoService(session)
        
        # 处理状态
        todo_status = None
        if status is not None:
            todo_status = TodoStatus(status)
        
        todos = service.get_todos(todo_status, category, deadline_before)
        
        if not todos:
            click.echo('没有找到匹配的待办事项')
            return
        
        # 准备表格数据
        table_data = []
        for t in todos:
            deadline_str = t.deadline.strftime('%Y-%m-%d %H:%M:%S') if t.deadline else ''
            table_data.append([
                t.id,
                t.content,
                t.category,
                t.tags or '',
                deadline_str,
                t.status.value,
                t.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # 打印表格
        headers = ['ID', '内容', '分类', '标签', '截止时间', '状态', '创建时间']
        click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
    except Exception as e:
        click.echo(f'查询待办事项失败：{str(e)}', err=True)

@todo_cli.command(name='delete', help='删除待办事项')
@click.option('--id', '-i', required=True, callback=validate_todo_id, help='待办事项ID')
def delete_todo(id):
    """删除待办事项命令"""
    try:
        session = db.get_session()
        service = TodoService(session)
        success = service.delete_todo(id)
        if success:
            click.echo(f'待办事项删除成功！ID: {id}')
        else:
            click.echo(f'待办事项不存在：ID {id}', err=True)
    except Exception as e:
        click.echo(f'删除待办事项失败：{str(e)}', err=True)
