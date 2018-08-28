import csv
from SendMessages import SendMessages


def parsCsv(numbers_file):
        with open(numbers_file) as f:
            out_list = []
            reader = csv.reader(f)
            for i in reader:
                out_list.append(i[0])
            return out_list
            
def textMessege(file):
    with open(file) as f:
        message = f.readlines()
        message = "".join(message)
        message = ''.join('%04X' % ord(c) for c in message)
        return message

def main():
    modem_param_file = "config.ini"
    message = textMessege('message.txt')
    numbers_file = 'test.csv'
    numbers_list = parsCsv(numbers_file)
    for number in numbers_list:
        number = "+" + str(number)
        send_msg=SendMessages(number, message, modem_param_file )
        send_msg.connectModem()
        send_msg.sendMessage()
        send_msg.disconnectModem()

if __name__ == '__main__':
    main()