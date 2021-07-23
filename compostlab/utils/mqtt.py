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
        self.client.connect("118.25.108.254", 1883, 60)

    def public_message(self, equipmentKey, msg, qos=0):
        self.client.publish(
            topic="compostlab/{}/response".format(equipmentKey), payload=msg, qos=qos)
