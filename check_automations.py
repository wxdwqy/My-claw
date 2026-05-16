import sqlite3
from datetime import datetime

conn = sqlite3.connect(r'C:\Users\wxd\AppData\Roaming\WorkBuddy\automations\automations.db')
cursor = conn.cursor()

# 查看所有自动化任务详细信息
cursor.execute('''SELECT id, name, status, cwds, rrule, next_run_at, last_run_at 
                  FROM automations ORDER BY name''')

print('=' * 80)
print('自动化任务详情')
print('=' * 80)

for row in cursor.fetchall():
    task_id, name, status, cwds, rrule, next_run, last_run = row
    print(f'\n【{name}】')
    print(f'  ID: {task_id}')
    print(f'  状态: {status}')
    print(f'  工作目录: {cwds}')
    print(f'  计划: {rrule}')
    
    if last_run:
        last_dt = datetime.fromtimestamp(last_run / 1000)
        print(f'  上次运行: {last_dt}')
    if next_run:
        next_dt = datetime.fromtimestamp(next_run / 1000)
        print(f'  下次运行: {next_dt}')

conn.close()
