import click
from .transaction_cli import transaction_cli
from .todo_cli import todo_cli

@click.group(name='cashlog', help='轻量化本地记账/待办CLI工具')
@click.version_option(version='0.1.0', prog_name='cashlog')
def main_cli():
    """主CLI入口"""
    pass

# 添加子命令组
main_cli.add_command(transaction_cli)
main_cli.add_command(todo_cli)

if __name__ == '__main__':
    main_cli()
