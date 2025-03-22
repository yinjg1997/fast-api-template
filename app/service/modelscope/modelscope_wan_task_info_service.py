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
file_name: modelscope_wan_task_info_service.py
"""
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

import pytz
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError

from app.dao import getDatabaseSession
from app.dao.models import ModelscopeWanTaskInfo

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ModelscopeWanTaskInfoService:
    """
    ModelscopeWanTaskInfo 服务类，用于处理 ModelscopeWanTaskInfo 表的数据库操作
    """

    def get_one_pending_task(self) -> Optional[ModelscopeWanTaskInfo]:
        """
        获取一条 task_status 为 'pending' 的记录

        :return: 一个 ModelscopeWanTaskInfo 对象或 None
        """
        with getDatabaseSession() as session:
            stmt = select(ModelscopeWanTaskInfo).where(ModelscopeWanTaskInfo.task_status == 'pending').order_by(
                ModelscopeWanTaskInfo.id)

            result = session.execute(stmt).scalars().first()
            return result

    def create(self, item_dict: Dict):
        """
        插入一条新的 ModelscopeWanTaskInfo 记录

        :param item_dict: 包含记录数据的字典
        """
        with getDatabaseSession() as session:
            try:
                new_item = ModelscopeWanTaskInfo(**item_dict)
                session.add(new_item)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def find_one(self, item_id: int) -> Optional[ModelscopeWanTaskInfo]:
        """
        读取一条 ModelscopeWanTaskInfo 记录

        :param item_id: 记录的 ID
        :return: ModelscopeWanTaskInfo 对象或 None
        """
        with getDatabaseSession() as session:
            return session.query(ModelscopeWanTaskInfo).filter_by(id=item_id).first()

    def update(self, id: int, item: ModelscopeWanTaskInfo):
        """
        更新一条 ModelscopeWanTaskInfo 记录

        :param id: 记录的 ID
        :param update_dict: 包含更新数据的字典
        """
        update_dict = {key: value for key, value in item.__dict__.items() if key != '_sa_instance_state'}

        with getDatabaseSession() as session:
            try:
                session.query(ModelscopeWanTaskInfo).filter_by(id=id).update(update_dict)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def delete(self, item_id: int):
        """
        删除一条 ModelscopeWanTaskInfo 记录

        :param item_id: 记录的 ID
        """
        with getDatabaseSession() as session:
            try:
                session.query(ModelscopeWanTaskInfo).filter_by(id=item_id).delete()
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def bulk_upsert(self, item_dicts: List[Dict]):
        """
        批量插入或更新 ModelscopeWanTaskInfo 记录

        :param item_dicts: 包含记录数据的字典列表
        """
        if not item_dicts:
            return

        stmt = insert(ModelscopeWanTaskInfo).values(item_dicts)

        columns = ModelscopeWanTaskInfo.__table__.columns.keys()

        update_dict = {column: stmt.inserted[column] for column in columns if column in item_dicts[0]}
        update_dict['updt_time'] = datetime.now(pytz.timezone('Asia/Shanghai'))

        stmt = stmt.on_duplicate_key_update(**update_dict)

        with getDatabaseSession() as session:
            try:
                session.execute(stmt)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise e
