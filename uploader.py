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


import os
import paho.mqtt.client
import time
import requests


dep_instance = os.getenv("DEP_INSTANCE")
job_callback_url = os.getenv("JOB_CALLBACK_URL")
ds_platform_id = os.getenv("DS_PLATFORM_ID")
ds_platform_type_id = os.getenv("DS_PLATFORM_TYPE_ID")
mqtt_server = os.getenv("mqtt_server")
mqtt_port = int(os.getenv("mqtt_port"))
mqtt_keepalive = int(os.getenv("mqtt_keepalive"))
usr = os.getenv("usr")
pw = os.getenv("pw")
service_id = os.getenv("service_id")
source_file = os.getenv("source_file")
data_cache_path = "/data_cache"


def on_connect(client, userdata, flags, rc):
    print("connected to '{}' on '{}'".format(mqtt_server, mqtt_port))


def on_disconnect(client, userdata, rc):
    print("disconnected from '{}'".format(mqtt_server, mqtt_port))


mqtt_client = paho.mqtt.client.Client(client_id=dep_instance)
mqtt_client.username_pw_set(username=usr, password=pw)
mqtt_client.tls_set()

mqtt_client.connect(
    host=mqtt_server,
    port=mqtt_port,
    keepalive=mqtt_keepalive
)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.loop_start()

print("publishing messages ...")
with open(os.path.join(data_cache_path, source_file), "r") as file:
    pub_count = 0
    for line in file:
        line = line.strip()
        while True:
            msg_info = mqtt_client.publish(topic=ds_platform_id + "/" + service_id, payload=line, qos=2)
            msg_info.wait_for_publish()
            if msg_info.rc == paho.mqtt.client.MQTT_ERR_SUCCESS:
                pub_count += 1
                break
            print("failed to publish message from line '{}'".format(pub_count))
            time.sleep(5)
print("published '{}' messages".format(pub_count))


mqtt_client.disconnect()

resp = requests.post(job_callback_url,json={dep_instance: None})
