"""
   Copyright 2021 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


__all__ = ("Config",)


import os


class Config:
    def __init__(self):
        self.data_cache_path = "/data_cache"
        self.dep_instance = os.getenv("DEP_INSTANCE")
        self.job_callback_url = os.getenv("JOB_CALLBACK_URL")
        self.ds_platform_id = os.getenv("DS_PLATFORM_ID")
        self.ds_platform_type_id = os.getenv("DS_PLATFORM_TYPE_ID")
        self.mqtt_server = os.getenv("mqtt_server")
        self.mqtt_port = os.getenv("mqtt_port")
        self.mqtt_keepalive = os.getenv("mqtt_keepalive")
        self.usr = os.getenv("usr")
        self.pw = os.getenv("pw")
        self.source_file_field = "source_file"
        self.service_id_field = "service_id"
        self.inputs = dict()
        for key, value in os.environ.items():
            if self.source_file_field in key:
                num = key.split("_", 2)[1]
                if num not in self.inputs:
                    self.inputs[num] = {self.source_file_field: value}
                else:
                    self.inputs[num][self.source_file_field] = value
            if self.service_id_field in key:
                num = key.split("_", 2)[1]
                if num not in self.inputs:
                    self.inputs[num] = {self.service_id_field: value}
                else:
                    self.inputs[num][self.service_id_field] = value
