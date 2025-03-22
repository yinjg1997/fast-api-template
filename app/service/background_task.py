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
import time
import uuid
from threading import Thread

import httpx
from loguru import logger

from app.service.modelscope import ModelscopeWanTaskInfoService, TaskStatus
from app.service.modelscope.wan_2_1 import Wan21Api, TaskType
from app.utils import change_file_ext, delete_file
from app.utils.aws_pub import S3, s3_prefix


def modelscope_wan21_task():
    wan_21_api = Wan21Api()
    modelscope_wan_task_info_service = ModelscopeWanTaskInfoService()
    s3 = S3()
    while True:
        try:
            task_info = modelscope_wan_task_info_service.get_one_pending_task()
            if task_info:
                task_info.hf_token = wan_21_api.hf_token
                # 处理任务
                if task_info.task_type == TaskType.T2V.value:
                    wan_21_api.switch_t2v_tab()
                    wan_21_api.t2v_generation_async(prompt=task_info.prompt, size=task_info.video_size,
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
                        start_time = time.time()
                        bar_res = wan_21_api.get_process_bar()
                        bar_value = bar_res.get("value")
                        if bar_value == 100:
                            cost_time_res = wan_21_api.cost_time()
                            status_res = wan_21_api.process_change()
                            status_value = status_res.get("value")
                            if status_value is None:
                                logger.warning(f"生成状态为 100, 但是 status_value 为 None")
                                status_value = {}

                            end_time = time.time()
                            task_info.cost_time = end_time - start_time

                            video_local_path = status_value.get("video", "")
                            logger.info("Background task completed.")

                            uuid_str = str(uuid.uuid4())
                            video_local_path = change_file_ext(file_path=video_local_path, basename=uuid_str,
                                                               new_ext='mp4')
                            # 上传至 S3
                            s3key = video_local_path
                            video_url = f"{s3_prefix}/{s3key}"
                            s3.upload_file(file_path=video_local_path, object_name=s3key)
                            delete_file(file_path=video_local_path)

                            task_info.video_url = video_url
                            task_info.task_status = TaskStatus.COMPLETED.value
                            modelscope_wan_task_info_service.update(id=task_info.id, item=task_info)

                            # todo 上传至飞书
                            break
                        else:
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
