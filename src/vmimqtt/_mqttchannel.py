import paho.mqtt.client as mqtt
from vmiiputil import getIpV4
import threading
import json
import time

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
    @property
    def on_connect(self):
        return self._onConnectCB

    @on_connect.setter
    def on_connect(self, cb):
        self._onConnectCB = cb
    
    @property
    def on_disconnect(self):
        return self._onDisConnectCB

    @on_disconnect.setter
    def on_disconnect(self, cb):
        self._onDisConnectCB = cb

    @property
    def on_message(self):
        return self._onMessageCB
    
    @on_message.setter
    def on_message(self, cb):
        self._onMessageCB = cb

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

class PingService:
    def __init__(self, deviceType, deviceId, brokerHost, brokerPort, brokerUserName, brokerPassword, interval=20, addIp=True) -> None:
        self._deviceType = deviceType
        self._deviceId = deviceId
        self._brokerHost = brokerHost
        self._brokerPort = brokerPort
        self._brokerUserName = brokerUserName
        self._brokerPassword = brokerPassword
        self._interval = interval
        self._addIp = addIp
        self._disconnectedEvent = threading.Event()
        self._connectedEvent = threading.Event()
        self._topic = "d2cping/{0}/{1}".format(self._deviceType, self._deviceId)
        self._channel = MqttChannel(host=brokerHost, 
                                    port=brokerPort, 
                                    username=brokerUserName, 
                                    password=brokerPassword)
        self._channel.on_connect = self._on_connected
        self._channel.on_disconnect = self._on_disconnected
        self._disconnectedEvent.set()
        self._isRunCalled = False
        self._client = None

    def _on_connected(self, client, userdata, falgs, rc):
        self._client = client
        self._connectedEvent.set()
        self._disconnectedEvent.clear()

    def _on_disconnected(self, client, userdata, rc):
        self._client = None
        self._connectedEvent.clear()
        self._disconnectedEvent.set()

    def Run(self):
        if self._isRunCalled is True:
            return
        self._isRunCalled = True
        self._channel.RunAsync()
        while True:
            pingMsg = {
                'interval': self._interval
            }
            if self._disconnectedEvent.wait(self._interval) is False:
                if self._addIp is True:
                    ipType, ipAddr = getIpV4()
                    if ipType is not None:
                        pingMsg['ip'] = ipAddr
                self._client.publish(topic=self._topic, payload=json.dumps(pingMsg),qos=0)
            else:
                time.sleep(1)


if __name__ == "__main__":
    p = PingService(
        deviceType="MockType",
        deviceId="01",
        brokerHost="localhost",
        brokerPort=1883,
        brokerUserName="mqtt_host:mqtt_test",
        brokerPassword="123456",
        addIp=False
    )
    p.Run()