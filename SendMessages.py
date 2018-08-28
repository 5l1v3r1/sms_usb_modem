import serial
import configparser
import random
from time import sleep

class SendMessages:
        
    def __init__(self, number, message, modem_param_file):
        '''Передача номер, текст сообщения и параметры подключения к модему'''
        self.number = number
        self.message = message
        self.modem_param_file = modem_param_file
        
    def connectModem(self):
        '''Покдлючаемся к модему'''
        Port, Baudrate, Timeout = self.confModem()  
        self.dev = serial.Serial(Port, int(Baudrate), timeout=int(Timeout))
        sleep(1)
        
    def confModem(self):
        '''Получаем параметры подключения'''
        conf = configparser.ConfigParser()
        conf.read(self.modem_param_file)
        self.port = conf.get("serial", "port")
        self.baudrate = conf.get("serial", "baudrate")
        self.timeout = conf.get("serial", "timeout")
        return self.port, self.baudrate, self.timeout
 
    def sendMessage(self):
        '''Отправка сообщения '''
        print("Wait is the message is sent to the number:%s" %self.number)
        timeout = round(random.uniform(1, 5),2)
        sleep(timeout)
        self.dev.write('ATZ\r'.encode())
        sleep(1)
        self.dev.write('AT+CMGF=1\r\n'.encode())
        sleep(1)
        self.dev.write('AT+CSCS="UTF-8"\r\n'.encode())
        sleep(1)
        self.dev.write('AT+CSMP=17,167,0,8\r\n'.encode())
        sleep(1)
        self.dev.write('AT+CMGS="{}"\r\n'.format(self.number).encode())
        sleep(1)
        self.dev.write(self.message.encode('utf-8'))
        sleep(1)
        self.dev.write(chr(26).encode())

    def disconnectModem(self):
        '''Закрытия соединения с модемом'''
        print("Closing the connection to the modem")
        self.dev.close()

