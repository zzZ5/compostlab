import json

from data.serializers import DataSerializer
from equipment.models import Equipment
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
        client.subscribe("compostlab/#")

    def on_message(self, client, userdata, msg):
        # The callback for when a PUBLISH message is received from the server.
        topic = msg.topic.split('/')
        if len(topic) < 4:
            print(topic)
            return
        if topic[0] != 'compostlab':
            return
        equipment_key = topic[1]
        method = topic[2]
        path = topic[3]
        data = json.loads(msg.payload)

        self.do_cmd(equipment_key, method, path, data)

    def public_message(self, equipmentKey, msg, qos=0):
        print(equipmentKey, msg)
        self.client.publish(
            topic="compostlab/{}/response".format(equipmentKey), payload=msg, qos=qos)

    def do_cmd(self, equipment_key, method, path, data):

        equipment = Equipment.objects.filter(key=equipment_key)
        if len(equipment) == 1:
            equipment = equipment[0]

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
