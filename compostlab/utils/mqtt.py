import django
import json
import os
from threading import Thread

from data.serializers import DataSerializer

import paho.mqtt.client as mqtt

# 为了能在外部脚本中调用Django ORM模型，必须配置脚本环境变量，将脚本注册到Django的环境变量中
# 第一个参数固定，第二个参数是工程名称.settings
os.environ.setdefault('DJANGO_SETTING_MODULE', 'compostlab.settings')
django.setup()


def public_message(equipmentKey, msg, qos=0):
    client.publish(
        topic="compostlab/{}/response".format(equipmentKey), payload=msg, qos=qos)


def on_connect(client, userdata, flags, rc):
    # The callback for when the client receives a CONNACK response from the server.
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("compostlab/#")


def on_message(client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server.
    topic = msg.topic.split('/')
    if len(topic) < 4:
        return
    if topic[0] != 'compostlab':
        return
    equipment_key = topic[1]
    method = topic[2]
    path = topic[3]
    data = json.loads(msg.payload)
    print(data)
    thread_do_cmd = Thread(target=do_cmd, args=(
        equipment_key, method, path, data))
    thread_do_cmd.start()


def do_cmd(equipment_key, method, path, data):

    if method == 'post':
        if path == 'data':
            if 'data' in data:
                serializer = DataSerializer(
                    data=data['data'], many=True)
            else:
                serializer = DataSerializer(data=data)
        if serializer.is_valid():
            # Successfully created
            serializer.save()
    else:
        return


# mqtt客户端启动函数
def mqttfunction():
    global client
    # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
    # client.loop_start()
    # client.loop_forever() 有掉线重连功能
    client.loop_forever(retry_first_connection=True)


client = mqtt.Client(client_id='zzZ5', clean_session=False)


def mqtt_run():
    client.username_pw_set(username='admin', password='L05b03j..')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("118.25.108.254", 1883, 60)
    client.loop_start()
    client.reconnect_delay_set(min_delay=1, max_delay=2000)
    # 启动
    mqttthread = Thread(target=mqttfunction)
    mqttthread.start()
