import click
from tabulate import tabulate
from datetime import datetime
from cashlog.data.database import db
from cashlog.service.transaction_service import TransactionService
from cashlog.data.models import TransactionType

def validate_amount(ctx, param, value):
    """验证金额是否为数字"""
    try:
        return float(value)
    except ValueError:
        raise click.BadParameter('金额需为数字')

def validate_date(ctx, param, value):
    """验证日期格式是否正确"""
    if value is None:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise click.BadParameter('日期格式需为 YYYY-MM-DD HH:MM:SS')

def validate_month(ctx, param, value):
    """验证月份是否在1-12之间"""
    if value is None:
        return None
    if 1 <= value <= 12:
        return value
    raise click.BadParameter('月份需在1-12之间')

def validate_year(ctx, param, value):
    """验证年份是否有效"""
    if value is None:
        return None
    current_year = datetime.now().year
    if 1900 <= value <= current_year + 10:
        return value
    raise click.BadParameter(f'年份需在1900-{current_year + 10}之间')

@click.group(name='transaction', help='收支记录管理命令')
def transaction_cli():
    """收支记录管理命令组"""
    pass

@transaction_cli.command(name='add', help='新增收支记录')
@click.option('--amount', '-a', required=True, callback=validate_amount, help='金额，正数为收入，负数为支出')
@click.option('--category', '-c', required=True, help='分类')
@click.option('--tags', '-t', help='标签，多个标签用逗号分隔')
@click.option('--remark', '-r', help='备注')
@click.option('--time', '-ti', callback=validate_date, help='交易时间，格式：YYYY-MM-DD HH:MM:SS')
def add_transaction(amount, category, tags, remark, time):
    """新增收支记录命令"""
    try:
        session = db.get_session()
        service = TransactionService(session)
        transaction = service.add_transaction(amount, category, tags, remark, time)
        click.echo(f'收支记录新增成功！ID: {transaction.id}')
    except Exception as e:
        click.echo(f'收支记录新增失败：{str(e)}', err=True)

@transaction_cli.command(name='list', help='查询收支记录')
@click.option('--month', '-m', type=int, callback=validate_month, help='月份')
@click.option('--year', '-y', type=int, callback=validate_year, help='年份')
@click.option('--category', '-c', help='分类')
@click.option('--tags', '-t', help='标签')
@click.option('--type', '-ty', type=click.Choice(['income', 'expense']), help='收支类型')
def list_transactions(month, year, category, tags, type):
    """查询收支记录命令"""
    try:
        session = db.get_session()
        service = TransactionService(session)
        
        # 处理收支类型
        transaction_type = None
        if type == 'income':
            transaction_type = TransactionType.INCOME
        elif type == 'expense':
            transaction_type = TransactionType.EXPENSE
        
        # 处理年份和月份的默认值
        if month is not None and year is None:
            year = datetime.now().year
        
        transactions = service.get_transactions(month, year, category, tags, transaction_type)
        
        if not transactions:
            click.echo('没有找到匹配的收支记录')
            return
        
        # 准备表格数据
        table_data = []
        for t in transactions:
            table_data.append([
                t.id,
                t.amount,
                t.category,
                t.tags or '',
                t.remark or '',
                t.transaction_time.strftime('%Y-%m-%d %H:%M:%S'),
                '收入' if t.type == TransactionType.INCOME else '支出'
            ])
        
        # 打印表格
        headers = ['ID', '金额', '分类', '标签', '备注', '交易时间', '类型']
        click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
    except Exception as e:
        click.echo(f'查询收支记录失败：{str(e)}', err=True)

@transaction_cli.command(name='summary', help='生成月度收支报表')
@click.option('--month', '-m', type=int, callback=validate_month, help='月份，默认当前月')
@click.option('--year', '-y', type=int, callback=validate_year, help='年份，默认当前年')
@click.option('--format', '-f', type=click.Choice(['text', 'markdown']), default='text', help='输出格式')
def monthly_summary(month, year, format):
    """生成月度收支报表命令"""
    try:
        # 设置默认年月
        current_date = datetime.now()
        if month is None:
            month = current_date.month
        if year is None:
            year = current_date.year
        
        session = db.get_session()
        service = TransactionService(session)
        summary = service.get_monthly_summary(month, year)
        
        if summary['transaction_count'] == 0:
            click.echo(f'{year}年{month}月没有交易记录')
            return
        
        if format == 'text':
            # 文本格式输出
            click.echo(f'=== {year}年{month}月收支报表 ===')
            click.echo(f'总收入：{summary["total_income"]:.2f} 元')
            click.echo(f'总支出：{summary["total_expense"]:.2f} 元')
            click.echo(f'结余：{summary["balance"]:.2f} 元')
            click.echo(f'交易笔数：{summary["transaction_count"]} 笔')
            click.echo('\n分类占比：')
            for cat, percentage in summary["category_percentage"].items():
                click.echo(f'  {cat}: {percentage}% ({summary["category_stats"][cat]:.2f} 元)')
        else:
            # Markdown格式输出
            click.echo(f'# {year}年{month}月收支报表')
            click.echo(f'| 项目 | 金额 |')
            click.echo(f'|------|------|')
            click.echo(f'| 总收入 | {summary["total_income"]:.2f} 元 |')
            click.echo(f'| 总支出 | {summary["total_expense"]:.2f} 元 |')
            click.echo(f'| 结余 | {summary["balance"]:.2f} 元 |')
            click.echo(f'| 交易笔数 | {summary["transaction_count"]} 笔 |')
            click.echo('\n## 分类占比')
            click.echo(f'| 分类 | 占比 | 金额 |')
            click.echo(f'|------|------|------|')
            for cat, percentage in summary["category_percentage"].items():
                click.echo(f'| {cat} | {percentage}% | {summary["category_stats"][cat]:.2f} 元 |')
    except Exception as e:
        click.echo(f'生成月度报表失败：{str(e)}', err=True)
