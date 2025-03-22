from datetime import datetime

import pytz
from sqlalchemy import Column, Index, String, TIMESTAMP, text, Integer, Text, Float, DateTime
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class YmUser(Base):
    __tablename__ = 'ym_user'
    __table_args__ = (
        Index('idx_nick_name', 'nick_name'),
        Index('idx_phone', 'phone'),
        {'comment': '用户表'}
    )

    id = Column(BIGINT, primary_key=True, comment='主键')
    union_id = Column(String(64), nullable=False, server_default=text("''"), comment='微信开放平台下的用户唯一标识')
    open_id = Column(String(64), nullable=False, server_default=text("''"), comment='微信openid')
    nick_name = Column(String(32), nullable=False, server_default=text("''"), comment='昵称')
    password = Column(String(64), nullable=False, server_default=text("''"), comment='密码')
    avatar = Column(String(255), nullable=False, server_default=text("''"), comment='头像')
    phone = Column(String(11), nullable=False, server_default=text("''"), comment='手机号')
    email = Column(String(50), nullable=False, server_default=text("''"), comment='电子邮箱')
    last_login = Column(String(20), nullable=False, server_default=text("''"), comment='上次登录时间')
    status = Column(TINYINT, nullable=False, server_default=text("'1'"), comment='状态；-1:黑名单 1:正常')
    delete_at = Column(String(20), nullable=False, server_default=text("''"), comment='删除时间')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')


class YmUserInfo(Base):
    __tablename__ = 'ym_user_info'
    __table_args__ = (
        Index('idx_uid', 'uid'),
        {'comment': '用户信息表'}
    )

    id = Column(BIGINT, primary_key=True, comment='主键')
    uid = Column(BIGINT, nullable=False, server_default=text("'0'"), comment='用户id')
    sex = Column(TINYINT, nullable=False, server_default=text("'-1'"), comment='性别；-1:未知 1:男 2:女 ')
    province = Column(VARCHAR(45), nullable=False, comment='省市')
    city = Column(VARCHAR(45), nullable=False, comment='城市')
    county = Column(VARCHAR(45), nullable=False, comment='区域')
    address = Column(String(255), nullable=False, server_default=text("''"), comment='详细地址')
    delete_at = Column(String(20), nullable=False, server_default=text("''"), comment='删除时间')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')

class ModelscopeWanTaskInfo(Base):
    __tablename__ = 'modelscope_wan_task_info'
    __table_args__ = (
        {'comment': 'modelscope wan 任务信息表'}
    )
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    hf_token = Column(String(255), comment='api token')

    task_type = Column(String(255), nullable=False, comment='任务类型 i2v | t2v')
    prompt = Column(Text, comment='提示词')
    video_size = Column(String(255), nullable=True, default='720*1280',
                        comment="t2v 视频尺寸 ['1280*720', '960*960', '720*1280', '1088*832', '832*1088']")

    image = Column(String(255), nullable=True, comment="i2v 图片 URL")
    model_type = Column(String(255), nullable=False,
                        comment="['wanx2.1-t2v-plus', 'wanx2.1-t2v-turbo'] ['wanx2.1-i2v-plus', 'wanx2.1-i2v-turbo']")

    seed = Column(Float, nullable=False, default=-1, comment="随机种子")

    task_status = Column(String(255), comment="任务状态 pending | progressing | completed")
    cost_time = Column(Float, comment="处理时间")
    video_url = Column(String(255), comment="生成的视频 URL")

    is_pushed = Column(String(10), comment="是否推送 0 | 1")

    inst_time = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), comment='记录创建时间')
    inst_user_no = Column(String(50), default="Spider", comment='记录创建用户')
    updt_time = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')),
                       onupdate=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), comment='记录更新时间')
    updt_user_no = Column(String(50), default="Spider", onupdate="Spider", comment='记录更新用户')