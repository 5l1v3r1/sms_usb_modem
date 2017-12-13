# -*- coding: utf-8 -*-

from time import sleep
import serial
import csv
import configparser


def pars_csv(filename):
    with open(filename) as f:
        out_list = []
        reader = csv.reader(f)
        for i in reader:
            out_list.append(i[0])
        return out_list


def send_msg(num=None, msg=None, dev=None):
    if num != "Close":
        sleep(10)
        dev.write('ATZ\r'.encode())
        dev.write('AT+CMGF=1\r\n'.encode())
        dev.write('AT+CSCS="UTF-8"\r\n'.encode())
        dev.write('AT+CSMP=17,167,0,8\r\n'.encode())
        dev.write('AT+CMGS="{}"\r\n'.format(num).encode())
        dev.write(msg)
        dev.write(chr(26).encode())
    else:
        print("Close connecting modem")
        dev.close()


def conf_get(filename):
    conf = configparser.ConfigParser()
    conf.read(filename)
    port = conf.get("serial", "port")
    baudrate = conf.get("serial", "baudrate")
    timeout = conf.get("serial", "timeout")
    return port, baudrate, timeout


def main():
    config_filename = "config.ini"
    conf = conf_get(config_filename)
    dev = serial.Serial(conf[0], int(conf[1]), timeout=int(conf[2]))
    msg = ''.join('%04X' % ord(c) for c in 'Привет')
    msg = msg.encode('utf-8')
    csv_file = 'test.csv'
    out_list = pars_csv(csv_file)

    for i in out_list:
        num = '+' + str(i)
        send_msg(num, msg, dev)
    else:
        send_msg(num="Close", dev=dev)


if __name__ == '__main__':
    main()
