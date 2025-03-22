# !/usr/bin/python
# coding: utf-8
"""
Version: v1.0
Main_function: 
para_remark:
develop_user: yuri
develop_date: 2025/3/22
execute_type:
execute_hz:
update_user:
update_date: 2025/3/22
file_name: file_util.py
"""
import os
from loguru import logger


def change_file_ext(file_path: str, new_ext: str = "mp4"):
    """
    修改文件扩展名
    """
    base = os.path.splitext(file_path)[0]
    new_file_path = f"{base}.{new_ext}"
    os.rename(file_path, new_file_path)
    return new_file_path

def delete_file(file_path: str):
    """
    删除文件
    """
    try:
        os.remove(file_path)
    except Exception as e:
        logger.error(f"An error occurred: {e}")