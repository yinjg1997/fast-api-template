# !/usr/bin/python
# coding: utf-8
"""
Version: v1.0
Main_function: 
para_remark:
develop_user: yuri
develop_date: 2025/2/19
execute_type:
execute_hz:
update_user:
update_date: 2025/2/19
file_name: lark_group_robot.py
"""
import base64
import hashlib
import hmac
import time

import requests


# 自测群
webhook = "https://open.larksuite.com/open-apis/bot/v2/hook/2fcc69c1-87a5-40d7-93ae-7a2a418e2c82"
secret = "5QFzvlA1YD2TTq251M4DVf"
class LarkGroupRobotService:
    """lark群机器人"""

    def __init__(self, webhook: str, secret: str):
        self.webhook = webhook
        self.secret = secret

    def create_sign(self) -> (int, str):
        """生成签名"""
        timestamp = int(time.time())
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return timestamp, sign

    def _send_req(self, data: dict):
        """统一发送请求"""
        timestamp, sign = self.create_sign()
        req_data = data.copy()
        req_data.update({'timestamp': timestamp, 'sign': sign})
        return requests.post(self.webhook, json=req_data).json()

    def send_card(self, card):
        """发送卡片消息"""
        data = {
            "msg_type": "interactive",
            "card": card
        }
        return self._send_req(data=data)

    def __hash__(self):
        return hash((self.webhook, self.secret))

    def __eq__(self, other):
        return (self.webhook, self.secret) == (other.webhook, other.secret)




if __name__ == '__main__':

    robot_debug = LarkGroupRobotService(
        webhook=webhook,
        secret=secret
    )

    md_rows = [
        {
            "project_name": "Project Alpha",
            "project_status": "Active",
            "news_type": "Long Form",
            "source_platform": "Website A",
            "title": "Introduction to Project Alpha",
            "content": "Project Alpha is an innovative solution...",
            "original_url": "https://websitea.com/article123"
        },
        {
            "project_name": "Project Beta",
            "project_status": "Completed",
            "news_type": "Long Form",
            "source_platform": "Website B",
            "title": "Completion of Project Beta",
            "content": "Project Beta has successfully achieved its goals...",
            "original_url": "https://websiteb.com/article456"
        },
        {
            "project_name": "Project Gamma",
            "project_status": "Pending",
            "news_type": "Long Form",
            "source_platform": "Website C",
            "title": "Upcoming Launch of Project Gamma",
            "content": "Project Gamma is set to launch soon...",
            "original_url": "https://websitec.com/article789"
        }
    ]

    # card = {
    #     "header": {
    #         "template": "blue",
    #         "title": {
    #             "content": "未上线项目的新闻匹配推送",
    #         }
    #     },
    #     "elements": [
    #         {
    #             "tag": "table",
    #             "page_size": 200,
    #             "row_height": "low",
    #             "header_style": {
    #                 "text_align": "center",
    #                 "text_size": "normal",
    #                 "background_style": "none",
    #                 "text_color": "grey",
    #                 "bold": True,
    #                 "lines": 1
    #             },
    #             "columns": [
    #                 {
    #                     "name": "project_name",
    #                     "display_name": "项目全称",
    #                     "width": "150px",
    #                     "data_type": "text",
    #                     "horizontal_align": "center",
    #                 },
    #                 {
    #                     "name": "project_status",
    #                     "display_name": "项目状态",
    #                     "width": "100px",
    #                     "data_type": "text",
    #                     "horizontal_align": "center"
    #                 },
    #                 {
    #                     "name": "news_type",
    #                     "display_name": "新闻类型",
    #                     "width": "100px",
    #                     "data_type": "text",
    #                     "horizontal_align": "center"
    #                 },
    #                 {
    #                     "name": "source_platform",
    #                     "display_name": "来源平台",
    #                     "width": "150px",
    #                     "data_type": "text",
    #                     "horizontal_align": "center"
    #                 },
    #                 {
    #                     "name": "title",
    #                     "display_name": "标题",
    #                     "width": "200px",
    #                     "data_type": "text",
    #                     "horizontal_align": "left"
    #                 },
    #                 {
    #                     "name": "content",
    #                     "display_name": "内容",
    #                     "width": "300px",
    #                     "data_type": "text",
    #                     "horizontal_align": "left"
    #                 },
    #                 {
    #                     "name": "original_url",
    #                     "display_name": "原文url",
    #                     "width": "200px",
    #                     "data_type": "text",
    #                     "horizontal_align": "left"
    #                 }
    #             ],
    #             "rows": md_rows
    #         }
    #     ]
    # }



    card = {
        "header": {
            "template": "blue",
            "title": {
                "content": "生成结果推送",
            }
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {"is_short": False, "text": {"tag": "lark_md", "content": f"**原文url：**{'original_url'}“"}},
                ]
            }
        ]
    }
    print(card)
    res = robot_debug.send_card(card=card)

    print(res)
