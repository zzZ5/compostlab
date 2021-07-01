import json

from data.serializers import DataSerializer
from sensor.models import Sensor

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
        self.client = mqtt.Client()
        self.client.username_pw_set(username='admin', password='L05b03j..')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("118.25.108.254", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        # The callback for when the client receives a CONNACK response from the server.

        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("topic/#")

    def on_message(self, client, userdata, msg):
        # The callback for when a PUBLISH message is received from the server.
        temp = msg.topic.split('/')
        if len(temp) < 2:
            return
        key = temp[1]
        data = json.loads(msg.payload)
        if(len(key) == 10):
            print(key)
            print(data)
        else:
            sensor = Sensor.objects.filter(key=key)
            if len(sensor) == 1:
                serializer = DataSerializer(data={**data, "key": key})
                serializer.save()

    def public_message(self, equipmentKey, msg, qos=0):
        # format {"cmd": "order"}
        self.client.publish(
            topic="topic/{}".format(equipmentKey), payload=msg, qos=qos)
