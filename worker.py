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


from uploader import Config
from uploader import Parser
import paho.mqtt.client
import requests


config = Config()


def on_connect():
    print("connected to '{}' on '{}'".format(config.mqtt_server, config.mqtt_port))


def on_disconnect():
    print("disconnected from '{}'".format(config.mqtt_server, config.mqtt_port))


mqtt_client = paho.mqtt.client.Client(client_id=config.dep_instance, clean_session=False)
mqtt_client.username_pw_set(username=config.usr, password=config.pw)
mqtt_client.tls_set()

mqtt_client.connect(
    host=config.mqtt_server,
    port=int(config.mqtt_port),
    keepalive=int(config.mqtt_keepalive)
)

mqtt_client.on_connect = on_connect
mqtt_client.disconnect = on_disconnect
mqtt_client.loop_start()

parser = Parser(
    ds_id=config.ds_platform_id,
    srv_id=config.service_id,
    file=config.source_file,
    dc_path=config.data_cache_path,
    client=mqtt_client
)
parser.run()

mqtt_client.disconnect()

resp = requests.post(config.job_callback_url,json={config.dep_instance: None})
