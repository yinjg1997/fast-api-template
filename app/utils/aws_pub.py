#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Version: v1.0
Main_function: AWS S3文件上传、获取、删除
para_remark:
develop_user: double_t、ck
develop_date: 2021-06-16
execute_type:
execute_hz:
update_user:
update_date:
"""

import os
import threading
from pathlib import Path
from queue import Queue
from boto3.session import Session
from botocore.client import Config
import requests

# 进程数
sem = threading.Semaphore(20)

s3endpoint = 'https://s3.bitiful.net' # 请填入控制台 “Bucket 设置” 页面底部的 “Endpoint” 标签中的信息
s3region = 'cn-east-1'
s3accessKeyId = 'vyt4LWvM7FB9mueN8qlwPKEh'
s3SecretKeyId = '3TBwPBt6h5llcryRSYA7j3JsGLKP7GC'


class S3(object):
    def __init__(self, access_key=s3accessKeyId, secret_key=s3SecretKeyId, bucket_name="ai-results"):
        """
        创建连接
        :param access_key: aws_access_key_id
        :param secret_key: aws_secret_access_key
        """
        session = Session(access_key, secret_key, region_name=s3region)
        self.bucket_name = bucket_name
        self.s3_client = session.client('s3', endpoint_url=s3endpoint)
        self.s3_bucket = session.resource('s3', endpoint_url=s3endpoint).Bucket(bucket_name)
        self.resource = session.resource('s3', endpoint_url=s3endpoint)
        self.q = Queue()
        print(1111)


    def _upload_file(self, file_path=None, object_name=None, que=None):
        """
        上传单个文件
        :param file_path: 需要上传的文件的名称(绝对路径)
        :param object_name: 需要上传到的路径，例如file/localfile/test
        :return:
        """
        with sem:
            if que is None and object_name is None:
                _, object_name = os.path.split(file_path)
            elif que:
                if not que.empty():
                    file_path = que.get()
                    _, object_name = os.path.split(file_path)
                else:
                    return
            try:
                self.s3_bucket.upload_file(Filename=file_path, Key=object_name)
                # print(object_name)
                # return "upload file success"
                return object_name
            except Exception as e:
                raise Exception(f"upload file error: {e.args}")

    def _upload_file_obj(self, file_obj, object_name, content_type='binary/octet-stream'):
        """
        上传二进制文件对象
        :param file_obj: 需要上传的文件对象
        :param object_name: 上传后的名称
        :return:
        """
        try:
            self.s3_bucket.upload_fileobj(Fileobj=file_obj, Key=object_name, ExtraArgs={"ContentType": content_type})
            return "upload file object success"
        except Exception as e:
            raise Exception(f"upload file object error: {e.args}")

    def upload_file(self, file_path=None, object_name=None, folder=None):
        """
        上传文件 传入folder时会循环上传整个文件夹
        :param file_path:
        :param object_name:
        :param folder:
        :return:
        """
        if folder is None:
            return self._upload_file(file_path, object_name)
        if not Path(folder).is_dir():
            raise Exception(f"传入了folder, 但是它不是一个文件夹路径")
        else:
            name = []
            file_list = os.listdir(folder)
            for file in file_list:
                file_path = os.path.join(folder, file)
                if not os.path.isfile(file_path):
                    file_list.remove(file)
                name_ = self._upload_file(file_path, file)
                name.append(name_)
            # return f"upload file total: {len(file_list)}"
            return name

    def upload_big_folder(self, folder):
        """
        处理数据量较大的文件夹上传
        :param folder: 文件夹路径
        :return:
        """
        file_list = os.listdir(folder)
        [self.q.put(os.path.join(folder, file)) for file in file_list]

        for _ in range(self.q.qsize()):
            tt = threading.Thread(target=self._upload_file, kwargs=({"que": self.q}), )
            tt.start()

    def delete_files(self, object_name):
        """
        删除文件
        :param object_name:
        :return:
        """
        try:
            if isinstance(object_name, str):
                object_list = [{"Key": object_name}]
            elif isinstance(object_name, list):
                object_list = [{"Key": i} for i in object_name]
            else:
                raise TypeError("object_name 只能传入str / list")
            self.s3_client.delete_objects(Bucket=self.bucket_name, Delete={"Objects": object_list})
            return "delete success"
        except Exception as e:
            raise Exception(f"delete file error: {e.args}")

    def get_obj_list(self):
        """
        列出桶内所有文件名
        :return:
        """
        return [obj.key for obj in self.s3_bucket.objects.all()]

    def check_file_exists(self, key: str) -> bool:
        """
        检查文件是否存在
        :param key: 文件的 S3 key
        :return: True 如果文件存在，否则 False
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except Exception as e:
            return False



if __name__ == '__main__':
    res = S3().upload_file(file_path='/Users/a1/Desktop/fast-api-template/Image-2-video 14B 720P.webp', object_name='1.webp')
    print(res)
