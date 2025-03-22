#!/usr/bin/python
# coding: utf-8
"""
Version: v1.0
Main_function: 调用视频处理和生成服务的API
para_remark: 包含API调用所需的参数说明
develop_user: yuri
develop_date: 2025/3/21
execute_type: 脚本执行
execute_hz: 按需执行
update_user:
update_date: 2025/3/21
file_name: Wan_2_1.py
"""
import time
from enum import Enum

from gradio_client import Client, handle_file
from typing import Dict, Optional, Union
from loguru import logger


class I2VModel(Enum):
    WANX_I2V_PLUS = 'wanx2.1-i2v-plus'
    WANX_I2V_TURBO = 'wanx2.1-i2v-turbo'


class T2VModel(Enum):
    WANX_T2V_PLUS = 'wanx2.1-t2v-plus'
    WANX_T2V_TURBO = 'wanx2.1-t2v-turbo'


class Resolution(Enum):
    RES_1280x720 = '1280*720'
    RES_960x960 = '960*960'
    RES_720x1280 = '720*1280'
    RES_1088x832 = '1088*832'
    RES_832x1088 = '832*1088'


class Wan21Api:
    base_url = "https://wan-ai-wan-2-1.ms.show/"

    def __init__(self):
        """
        初始化API客户端。

        :param base_url: API的基础URL
        :param hf_token: 身份验证令牌
        """
        self.hf_token = "7087a490-63e7-48a5-923d-68645fddc0fc"
        self.client = Client(self.base_url, hf_token=self.hf_token)

    def change_hf_token(self, hf_token: str) -> None:
        """
        调用/change_hf_token端点，更换身份验证令牌。

        :param hf_token: str, 必需。新的身份验证令牌。
        """
        # todo 在 token 库中查找能用的令牌
        self.client = Client(self.base_url, hf_token=self.hf_token)

    def process_change(self) -> Dict[str, Union[str, None]]:
        """
        调用/process_change端点。

        :return: 返回处理结果的字典
        """
        result = self.client.predict(api_name="/process_change")
        logger.debug(result)
        return result

    def switch_i2v_tab(self) -> None:
        """
        调用/switch_i2v_tab端点，切换到i2v选项卡。
        """
        res = self.client.predict(api_name="/switch_i2v_tab")
        logger.debug(res)

    def switch_t2v_tab(self) -> None:
        """
        调用/switch_t2v_tab端点，切换到t2v选项卡。
        """
        self.client.predict(api_name="/switch_t2v_tab")

    def t2v_generation_async(self, prompt: str, size: str = "1280*720",
                             watermark_wanx: bool = False, model: str = "wanx2.1-t2v-plus",
                             seed: float = -1) -> Dict:
        """
        调用/t2v_generation_async端点进行文本到视频异步生成。

        可传参数:
        :param prompt: str, 必需。提供给"Prompt"文本框组件的输入值。
        :param size: Literal['1280*720', '960*960', '720*1280', '1088*832', '832*1088'], 默认值: "1280*720"。提供给"Resolution"下拉组件的输入值。
        :param watermark_wanx: bool, 默认值: True。提供给"Watermark"复选框组件的输入值。
        :param model: Literal['wanx2.1-t2v-plus', 'wanx2.1-t2v-turbo'], 默认值: "wanx2.1-t2v-plus"。提供给"Model"下拉组件的输入值。
        :param seed: float, 默认值: -1。提供给"Seed"数字组件的输入值。

        :return: 返回生成结果的字典
        生成的文件在 '/private/var/folders/77/bf_t9v_n4lv814tj8_tn_g740000gn/T/gradio/‘ 目录下
        """
        result = self.client.predict(
            prompt=prompt,
            size=size,
            watermark_wanx=watermark_wanx,
            model=model,
            seed=seed,
            api_name="/t2v_generation_async"
        )
        logger.debug(result)
        return result

    def i2v_generation_async(self, prompt: str, image_path: str,
                             watermark_wanx: bool = False, model: str = "wanx2.1-i2v-plus",
                             seed: float = -1) -> Dict:
        """
        调用/i2v_generation_async端点进行图像到视频异步生成。

        可传参数:
        :param prompt: str, 默认值: ""。提供给"Prompt"文本框组件的输入值。
        :param image: Dict, 必需。提供给"Upload Input Image"图像组件的输入值。对于输入，必须提供path或url之一。输出时，总是提供path。
            - path: str | None (本地文件路径)
            - url: str | None (公开可用的URL或base64编码的图像)
            - size: int | None (图像的字节大小)
            - orig_name: str | None (原始文件名)
            - mime_type: str | None (图像的MIME类型)
            - is_stream: bool (总是可以设置为False)
            - meta: Dict()
        :param watermark_wanx: bool, 默认值: True。提供给"Watermark"复选框组件的输入值。
        :param model: Literal['wanx2.1-i2v-plus', 'wanx2.1-i2v-turbo'], 默认值: "wanx2.1-i2v-plus"。提供给"Model"下拉组件的输入值。
        :param seed: float, 默认值: -1。提供给"Seed"数字组件的输入值。

        :return: 返回生成结果的字典
        """
        image = handle_file(image_path)
        result = self.client.predict(
            prompt=prompt,
            image=image,
            watermark_wanx=watermark_wanx,
            model=model,
            seed=seed,
            api_name="/i2v_generation_async"
        )
        logger.debug(result)
        return result

    def cost_time(self) -> float:
        """
        调用/cost_time端点，获取处理时间。

        :return: 返回处理时间
        """
        result = self.client.predict(api_name="/cost_time")
        logger.debug(result)
        return result

    def get_process_bar(self) -> dict:
        """
        调用/get_process_bar端点，获取进度条状态。

        :return: 返回进度条状态

        {'__type__': 'update', 'value': {'subtitles': None, 'video': '/private/var/folders/77/bf_t9v_n4lv814tj8_tn_g740000gn/T/gradio/434b30ee16ca854c2aba623f8ff2547376f2297b617f37b95122270acd1e675d/3d67b1e4-229d-4b0a-a73b-942c0bdad4b4.mp4Expires1742719724OSSAccessKeyIdLTAI5tKPD3TMqf2Lna1fASuhSignature56bxv7Ec0MB2xdWa1A2BTeCKAUnI3D'}}
        """
        result = self.client.predict(api_name="/get_process_bar")
        logger.debug(result)
        return result


if __name__ == '__main__':
    # 使用示例
    api = Wan21Api()
    api.switch_t2v_tab()
    prompt = """
    主题：卡通鸡（红色鸡冠和肉垂，简约线条）
    场景：浅米色背景（简单而突出角色）
    动作：鸡啄食虫子（虫子用弯曲线条表示运动）
    镜头语言：中景镜头，聚焦在鸡与虫子的互动
    氛围：轻松、幽默
    风格：手绘简约风格
    """
    api.t2v_generation_async(prompt=prompt, size=Resolution.RES_720x1280.value, model=T2VModel.WANX_T2V_PLUS.value,
                             seed=-1)

    while True:
        api.get_process_bar()
        api.process_change()
        time.sleep(5)
