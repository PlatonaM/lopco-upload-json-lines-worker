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
import socket
import time
import requests
import socks


dep_instance = os.getenv("DEP_INSTANCE")
job_callback_url = os.getenv("JOB_CALLBACK_URL")
ds_platform_id = os.getenv("DS_PLATFORM_ID")
ds_platform_type_id = os.getenv("DS_PLATFORM_TYPE_ID")
mqtt_server = os.getenv("mqtt_server")
mqtt_port = int(os.getenv("mqtt_port"))
mqtt_keepalive = int(os.getenv("mqtt_keepalive") or 5)
mqtt_qos = int(os.getenv("mqtt_qos") or 2)
mqtt_con_retry = int(os.getenv("mqtt_connect_retry") or 10)
mqtt_con_retry_delay = int(os.getenv("mqtt_connect_retry_dealy") or 30)
usr = os.getenv("usr")
pw = os.getenv("pw")
service_id = os.getenv("service_id")
source_file = os.getenv("source_file")
proxy_type = os.getenv("proxy_type")
proxy_addr = os.getenv("proxy_address")
proxy_usr = os.getenv("proxy_usr")
proxy_pw = os.getenv("proxy_pw")
data_cache_path = "/data_cache"


proxy_type_map = {
    "HTTP": socks.HTTP,
    "SOCKS4": socks.SOCKS4,
    "SOCKS5": socks.SOCKS5
}


def on_connect(client, userdata, flags, rc):
    print("connected to '{}' on '{}'".format(mqtt_server, mqtt_port))


def on_disconnect(client, userdata, rc):
    print("disconnected from '{}'".format(mqtt_server, mqtt_port))


mqtt_client = paho.mqtt.client.Client(client_id=dep_instance)
mqtt_client.username_pw_set(username=usr, password=pw)
mqtt_client.tls_set()

if proxy_addr and proxy_type:
    proxy_args = {
        "proxy_type": proxy_type_map[proxy_type],
        "proxy_addr": proxy_addr
    }
    if proxy_usr:
        proxy_args["proxy_username"] = proxy_usr
    if proxy_pw:
        proxy_args["proxy_password"] = proxy_pw
    mqtt_client.proxy_set(**proxy_args)


print("connecting ...")
tries = 0
while True:
    try:
        mqtt_client.connect(
            host=mqtt_server,
            port=mqtt_port,
            keepalive=mqtt_keepalive
        )
        break
    except (socket.timeout, OSError) as ex:
        if tries >= mqtt_con_retry:
            raise ex
        tries += 1
        print("connecting failed - {} - retry in {}s".format(ex, mqtt_con_retry_delay * (tries)))
        time.sleep(mqtt_con_retry_delay * (tries + 1))

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.loop_start()

line_count = 0
with open(os.path.join(data_cache_path, source_file), "r") as file:
    for line in file:
        line_count += 1

p = 1
steps = 100 / p
prog_step = int(line_count / steps)


def calc_time(s_t, p_c):
    t = (time.time() - s_t) * (steps - int(p_c / prog_step))
    if t < 60:
        return "{}s".format(round(t, 2))
    if t < 3600:
        return "{}m".format(round(t / 60, 2))
    return "{}h".format(round(t / 3600, 2))


print("publishing messages ...")
pub_count = 0
prog_count = 0
srt_time = time.time()
with open(os.path.join(data_cache_path, source_file), "r") as file:
    for line in file:
        line = line.strip()
        while True:
            msg_info = mqtt_client.publish(topic=ds_platform_id + "/" + service_id, payload=line, qos=mqtt_qos)
            msg_info.wait_for_publish()
            if msg_info.rc == paho.mqtt.client.MQTT_ERR_SUCCESS:
                prog_count += 1
                break
            print("failed to publish message from line '{}'".format(pub_count))
            time.sleep(5)
        if prog_count == prog_step:
            pub_count += prog_count
            done_p = int(pub_count / prog_step) * p
            if done_p < 100:
                print("{}% (estimated time remaining: {})".format(str(done_p).zfill(3), calc_time(srt_time, pub_count)))
            prog_count = 0
            srt_time = time.time()
if prog_count < prog_step:
    pub_count += prog_count
if not pub_count:
    pub_count = prog_count
print("100%")
print("published '{}' messages".format(pub_count))

mqtt_client.disconnect()

resp = requests.post(job_callback_url,json={dep_instance: None})
