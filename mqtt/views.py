from django.http import HttpResponse
from compostlab.utils.mqtt import Mqtt


def startMqtt(request):
    mqtt = Mqtt()
    return HttpResponse("Mqtt client started!.")
