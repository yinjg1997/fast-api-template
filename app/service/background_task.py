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

from app.service.modelscope import ModelscopeWanTaskInfoService, TaskStatus
from app.service.modelscope.wan_2_1 import Wan21Api, TaskType
from app.utils import change_file_ext, delete_file


def modelscope_wan21_task():
    wan_21_api = Wan21Api()
    modelscope_wan_task_info_service = ModelscopeWanTaskInfoService()
    while True:
        try:
            task_info = modelscope_wan_task_info_service.get_one_pending_task()
            if task_info:
                # 处理任务
                if task_info.task_type == TaskType.T2V.value:
                    wan_21_api.switch_t2v_tab()
                    wan_21_api.t2v_generation_async(prompt=task_info.prompt, size=task_info.task_size,
                                                    model=task_info.model_type, seed=task_info.seed)
                elif task_info.task_type == TaskType.I2V.value:
                    wan_21_api.switch_i2v_tab()
                    wan_21_api.i2v_generation_async(prompt=task_info.prompt, image_path=task_info.image,
                                                    model=task_info.model_type, seed=task_info.seed, )

                # 修改状态
                task_info.task_status = TaskStatus.PROCESSING.value
                modelscope_wan_task_info_service.update(id=task_info.id, item=task_info)

                # 监听任务进度
                while True:
                    try:
                        # cost_time_res = wan_21_api.cost_time()
                        bar_res = wan_21_api.get_process_bar()
                        status_res = wan_21_api.process_change()

                        bar_value = bar_res.get("value")
                        video_local_path = status_res.get("value", {}).get("video")
                        if bar_value == 100 and video_local_path:
                            logger.info("Background task completed.")
                            """
                            todo
                            上传至 S3
                            删除本地文件
                            更新任务状态, video_url
                            """
                            video_local_path = change_file_ext(file_path=video_local_path, new_ext='mp4')
                            # todo 上传至 S3
                            s3key = ""
                            video_url = ""
                            # delete_file(file_path=video_local_path)

                            task_info.video_url = video_url
                            task_info.task_status = TaskStatus.COMPLETED.value
                            modelscope_wan_task_info_service.update(id=task_info.id, item=task_info)
                            break

                        time.sleep(10)
                    except httpx.TimeoutException:
                        logger.info("Request timed out.")
                    except Exception as e:
                        logger.error(e)
            else:
                # 如果没有任务就休眠 60 s
                logger.debug(f"No pending tasks, sleeping for 60 seconds.")
                time.sleep(60)
        except Exception as e:
            logger.error(e)


def start_background_task():
    thread = Thread(target=modelscope_wan21_task, daemon=True)
    thread.start()
