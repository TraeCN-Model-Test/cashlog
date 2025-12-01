# cashlog 控制台输出样例

## 1. 帮助信息

### 主命令帮助
```bash
$ uv run python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  轻量化本地记账/待办CLI工具

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  todo         待办事项管理
  transaction  收支记录管理
```

### 收支管理命令帮助
```bash
$ uv run python main.py transaction --help
Usage: main.py transaction [OPTIONS] COMMAND [ARGS]...

  收支记录管理

Options:
  --help  Show this message and exit.

Commands:
  add      新增收支记录
  list     查询收支记录
  summary  生成月度收支报表
```

### 待办管理命令帮助
```bash
$ uv run python main.py todo --help
Usage: main.py todo [OPTIONS] COMMAND [ARGS]...

  待办事项管理

Options:
  --help  Show this message and exit.

Commands:
  add     新增待办事项
  delete  删除待办事项
  list    查询待办事项
  update  更新待办状态
```

## 2. 新增记录

### 新增收入记录
```bash
$ uv run python main.py transaction add -a 1000 -c 工资 -t 收入,工资 -r 2024年1月工资
收支记录添加成功！
```

### 新增支出记录
```bash
$ uv run python main.py transaction add -a -500 -c 餐饮 -t 支出,餐饮 -r 午餐
收支记录添加成功！
```

### 新增待办事项
```bash
$ uv run python main.py todo add -c 完成项目报告 -ca 工作 -d 2024-01-15 18:00:00
待办事项添加成功！ID: 1
```

## 3. 查询记录

### 查询所有收支记录
```bash
$ uv run python main.py transaction list
+----+------------+-------+------+--------+--------+---------------------+
| ID |    日期    | 金额  | 分类 |  标签  | 备注   |      创建时间       |
+----+------------+-------+------+--------+--------+---------------------+
| 1  | 2024-01-01 | 1000.0| 工资 | 收入,工资 | 2024年1月工资 | 2024-01-01 10:00:00 |
| 2  | 2024-01-02 | -500.0| 餐饮 | 支出,餐饮 | 午餐     | 2024-01-02 12:00:00 |
+----+------------+-------+------+--------+--------+---------------------+
```

### 查询2024年1月的收支记录
```bash
$ uv run python main.py transaction list -m 1 -y 2024
+----+------------+-------+------+--------+--------+---------------------+
| ID |    日期    | 金额  | 分类 |  标签  | 备注   |      创建时间       |
+----+------------+-------+------+--------+--------+---------------------+
| 1  | 2024-01-01 | 1000.0| 工资 | 收入,工资 | 2024年1月工资 | 2024-01-01 10:00:00 |
| 2  | 2024-01-02 | -500.0| 餐饮 | 支出,餐饮 | 午餐     | 2024-01-02 12:00:00 |
+----+------------+-------+------+--------+--------+---------------------+
```

### 查询所有待办事项
```bash
$ uv run python main.py todo list
+----+----------------+--------+------+---------------------+--------+---------------------+
| ID |     内容       | 分类   | 标签 |     截止时间        | 状态   |      创建时间       |
+----+----------------+--------+------+---------------------+--------+---------------------+
| 1  | 完成项目报告   | 工作   |      | 2024-01-15 18:00:00 | todo   | 2024-01-01 14:00:00 |
+----+----------------+--------+------+---------------------+--------+---------------------+
```

### 查询状态为todo的待办事项
```bash
$ uv run python main.py todo list -s todo
+----+----------------+--------+------+---------------------+--------+---------------------+
| ID |     内容       | 分类   | 标签 |     截止时间        | 状态   |      创建时间       |
+----+----------------+--------+------+---------------------+--------+---------------------+
| 1  | 完成项目报告   | 工作   |      | 2024-01-15 18:00:00 | todo   | 2024-01-01 14:00:00 |
+----+----------------+--------+------+---------------------+--------+---------------------+
```

## 4. 更新记录

### 更新待办状态为doing
```bash
$ uv run python main.py todo update -i 1 -s doing
待办状态更新成功！
```

### 更新待办状态为done
```bash
$ uv run python main.py todo update -i 1 -s done
待办状态更新成功！
```

## 5. 删除记录

### 删除待办事项
```bash
$ uv run python main.py todo delete -i 1
待办事项删除成功！
```

## 6. 生成报表

### 生成月度收支报表（文本格式）
```bash
$ uv run python main.py transaction summary -m 1 -y 2024
2024年1月收支报表

收支汇总：
总收入：1000.00
总支出：500.00
结余：500.00

分类占比：
工资：1000.00 (66.67%)
餐饮：-500.00 (33.33%)
```

### 生成月度收支报表（Markdown格式）
```bash
$ uv run python main.py transaction summary -m 1 -y 2024 -f markdown
# 2024年1月收支报表

## 收支汇总
| 项目   | 金额   |
|--------|--------|
| 总收入 | 1000.00|
| 总支出 | 500.00 |
| 结余   | 500.00 |

## 分类占比
| 分类   | 金额   | 占比   |
|--------|--------|--------|
| 工资   | 1000.00| 66.67% |
| 餐饮   | -500.00| 33.33% |
```

## 7. 错误提示

### 无效金额
```bash
$ uv run python main.py transaction add -a abc -c 工资
错误：金额需为数字
```

### 无效日期
```bash
$ uv run python main.py transaction add -a 1000 -c 工资 -d 2024-13-01
错误：日期格式无效，请使用YYYY-MM-DD格式
```

### 无效待办状态
```bash
$ uv run python main.py todo update -i 1 -s invalid
错误：状态无效，必须是todo/doing/done
```

### ID不存在
```bash
$ uv run python main.py todo update -i 999 -s doing
错误：待办事项不存在
```

### 查询无数据
```bash
$ uv run python main.py transaction list -m 2 -y 2024
暂无收支记录
```
