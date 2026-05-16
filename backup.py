# -*- coding: utf-8 -*-
"""
备份脚本 - 同步 scripts 和 projects 到百度网盘
用法: py -X utf8 scripts/backup.py
"""
import shutil
import os
from datetime import datetime

# 源文件夹
CLAW_ROOT = r"C:\Users\wxd\WorkBuddy\Claw"
SCRIPTS_SRC = os.path.join(CLAW_ROOT, "scripts")
PROJECTS_SRC = os.path.join(CLAW_ROOT, "projects")

# 目标文件夹（百度网盘同步）
BAIDU_ROOT = r"D:\BaiduSyncdisk\Workbuddy"
SCRIPTS_DST = os.path.join(BAIDU_ROOT, "scripts")
PROJECTS_DST = os.path.join(BAIDU_ROOT, "projects")

def backup_folder(src, dst, name):
    """备份单个文件夹"""
    if not os.path.exists(src):
        print(f"[跳过] {name}: 源文件夹不存在")
        return

    # 如果目标已存在，先删除
    if os.path.exists(dst):
        shutil.rmtree(dst)

    # 复制
    shutil.copytree(src, dst)
    file_count = len([f for f in os.listdir(dst) if os.path.isfile(os.path.join(dst, f))])
    print(f"[备份] {name}: {file_count} 个文件 -> {dst}")

def main():
    now = datetime.now()
    print(f"\n{'='*50}")
    print(f"云爪备份任务 - {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    backup_folder(SCRIPTS_SRC, SCRIPTS_DST, "Python脚本")
    backup_folder(PROJECTS_SRC, PROJECTS_DST, "物理动画")

    print(f"\n{'='*50}")
    print(f"备份完成！文件已同步到百度网盘")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
