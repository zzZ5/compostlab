import json
from threading import Thread

from data.serializers import DataSerializer
from django.http import HttpResponse

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
        self.client = mqtt.Client(client_id='zzZ5', clean_session=True)
        self.client.username_pw_set(username='admin', password='L05b03j..')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("118.25.108.254", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        # The callback for when the client receives a CONNACK response from the server.
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("compostlab/#")

    def on_message(self, client, userdata, msg):
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
        # print(data)
        thread_do_cmd = Thread(target=do_cmd, args=(
            equipment_key, method, path, data))
        thread_do_cmd.start()


def do_cmd(equipment_key, method, path, data):

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
    else:
        return


def startMqtt(request):
    mqtt = Mqtt()
    return HttpResponse("Mqtt client started!.")
