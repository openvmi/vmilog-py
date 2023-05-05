import paho.mqtt.client as mqtt
from vmiiputil import getIpV4

class MqttChannel:
    def __init__(self, host, port, username, password) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._onConnectCB = None
        self._onDisConnectCB = None
        self._onMessageCB = None
        self._client = None

    def _onConnect(self, client, userdata, flags, rc):
        if self._onConnectCB is not None:
            self._onConnectCB(client, userdata, flags, rc)

    def _onDisconnect(self, client, userdata, rc):
        if self._onDisConnectCB is not None:
            self._onDisConnectCB(client, userdata, rc)
    
    def _onMessage(self, client, userdata, message):
        if self._onMessageCB is not None:
            self._onMessageCB(client, userdata, message)

    def Run(self):
        while True:
            self._client = mqtt.Client()
            self._client.on_connect = self._onConnect
            self._client.on_disconnect = self._onDisconnect
            self._client.on_message = self._onMessage
            self._client.username_pw_set(username=self._username, password=self._password)
            try:
                self._client.connect(host=self._host, port=self._port, keepalive=60)
            except Exception as e:
                print(e)
            self._client.loop_forever(retry_first_connection=True)

    def RunAsync(self):
        while True:
            self._client = mqtt.Client()
            self._client.on_connect = self._onConnect
            self._client.on_disconnect = self._onDisconnect
            self._client.on_message = self._onMessage
            self._client.username_pw_set(username=self._username, password=self._password)
            try:
                self._client.connect(host=self._host, port=self._port, keepalive=60)
            except Exception as e:
                print(e)
            self._client.loop_start()

def StartPing(deviceType, deviceId, brokerHost, brokerPort, brokerUserName, brokerPassword, interval=20, addIp=True):
    topic = "d2cping/{0}/{1}".format(deviceType, deviceId)
    pingMsg = {
        'interval': 20
    }
    if addIp is True:
        ipType, ipAddr = getIpV4()
        if ipType is not None:
            pingMsg['ip'] = ipAddr

    channel = MqttChannel(host=brokerHost, 
                          port=brokerPort, 
                          username=brokerUserName, 
                          password=brokerPort)


