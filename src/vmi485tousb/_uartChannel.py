import serial
import threading

class UartChannel:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=3) -> None:
        self._baudrate = baudrate
        self._port = port
        self._timeout = timeout
        self._serial = None
        self._lock = threading.Lock()
        setattr(self, 'queryValue', self._realQueryValue)

    def endableMock(self):
        setattr(self, 'queryValue', self._mockQueryValue)

    def disableMock(self):
        setattr(self, 'queryValue', self._realQueryValue)
        
    def queryValue(self, command, responseLength):
        pass

    def _realQueryValue(self, command, responseLength):
        with self._lock:
            if self._serial is None or self._serial.is_open is False:
                try:
                    self._serial = serial.Serial(self._port, self._baudrate, timeout=self._timeout)
                except serial.SerialException:
                    print("error in open serial channel")
                    return None
            try:
                hasAttr = getattr(self._serial, 'flushInput', None)
                if hasAttr is not None:
                    self._serial.flushInput()
                else:
                    self._serial.reset_input_buffer()
                self._serial.write(command)
            except serial.SerialTimeoutException:
                return None
            value = self._serial.read(responseLength)
            return value
    
    def _mockQueryValue(self, command, responseLength):
        ret = []
        for i in range(responseLength):
            ret.append(i)
        return bytes(ret)
