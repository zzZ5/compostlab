# scripts/mqtt.py
# 脚本文件，需要使用`python manage.py runscript mqtt`指令方可运行
# 详情参见 https://django-extensions-zh.readthedocs.io/zh_CN/latest/runscript.html

import json
from threading import Thread

from data.serializers import DataSerializer

from django.core.mail import send_mail
import paho.mqtt.client as mqtt


class Singleton():
    # 类装饰器实现单例模式
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        # 类被调用时会触发此方法
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


@Singleton
class Mqtt():
    def __init__(self):
        self.client = mqtt.Client(client_id='zzZ5', clean_session=False)
        self.client.username_pw_set(username='admin', password='L05b03j..')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("118.25.108.254", 1883, 60)

    def start(self):
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        # The callback for when the client receives a CONNACK response from the server.
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        # 监听 compostlab下的所有topic
        client.subscribe("compostlab/#")

    def on_message(self, client, userdata, msg):
        # The callback for when a PUBLISH message is received from the server.
        '''
        topic一般组成为 compostlab/{key}/{method}/{path}
        其中 key: 设备key或者传感器key。
            method: 和equest的method类似。
            path: 其他指令
        '''

        topic = msg.topic.split('/')
        # print(topic)
        if len(topic) < 4:
            return
        if topic[0] != 'compostlab':
            return
        equipment_key = topic[1]
        method = topic[2]
        path = topic[3]
        try:
            data = json.loads(msg.payload)
        except:
            data = {}
        # print(data)

        # 新建一个线程处理接受到的信息
        thread_do_cmd = Thread(target=do_cmd, args=(
            equipment_key, method, path, data))
        thread_do_cmd.start()

    def public_message(self, equipmentKey, msg, qos=0):
        self.client.publish(
            topic="compostlab/{}/response".format(equipmentKey), payload=msg, qos=qos)


def do_cmd(equipment_key, method, path, data):
    # 处理接收到的信息。

    # equipment = Equipment.objects.filter(key=equipment_key)
    # if len(equipment) == 1:
    #     equipment = equipment[0]

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
    elif method == 'alert':
        print(send_mail('alert', equipment_key + ": " + str(data), 'baoju_liu@foxmail.com',
                        ['1450791278@qq.com']))
    else:
        return


def run():
    my_mqtt = Mqtt()
    my_mqtt.start()
