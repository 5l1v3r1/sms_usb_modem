# -*- coding: utf-8 -*-

from time import sleep
import serial
import csv


def pars_csv(filename):
    with open(filename) as f:
        out_list = []
        reader = csv.reader(f)
        for i in reader:
            out_list.append(i[0])
        return out_list


def send_msg(num, msg):
    sleep(10)
    device = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
    device.write('ATZ\r'.encode())
    device.write('AT+CMGF=1\r\n'.encode())
    device.write('AT+CSCS="UTF-8"\r\n'.encode())
    device.write('AT+CSMP=17,167,0,8\r\n'.encode())
    device.write('AT+CMGS="{}"\r\n'.format(num).encode())
    device.write(msg)
    device.write(chr(26).encode())
    device.close()


def main():
    msg = ''.join('%04X' % ord(c) for c in 'Привет')
    msg = msg.encode('utf-8')
    csv_file = 'test.csv'
    out_list = pars_csv(csv_file)
    for i in out_list:
        num = '+' + str(i)
        send_msg(num, msg)


if __name__ == '__main__':
    main()
