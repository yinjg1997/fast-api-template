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
file_name: background_task.py
"""
from threading import Thread
import time

import httpx
from loguru import logger

from app.service.modelscope.Wan_2_1 import Wan21Api


def background_task(wan_21_api: Wan21Api):
    while True:
        try:
            logger.debug("Running background task...")
            bar_res = wan_21_api.get_process_bar()
            status_res = wan_21_api.process_change()

            bar_value = bar_res.get("value")
            status_value = status_res.get("value", {}).get("video")
            if bar_value == 100 and status_value:
                logger.info("Background task completed.")
                # todo 从数据库中取出下一个任务
                # wan_21_api.switch_t2v_tab()

            time.sleep(5)
        except httpx.TimeoutException:
            logger.info("Request timed out.")
        except Exception as e:
            logger.error(e)

def start_background_task():
    wan_21_api = Wan21Api()
    thread = Thread(target=background_task, args=(wan_21_api,),daemon=True)
    thread.start()
