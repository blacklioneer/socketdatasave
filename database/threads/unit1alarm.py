from socket import *
import time
global flag, Num
from multiprocessing import Process, Pipe
Num=0
flag = 0
global i
i = 0


def unit1alarm(childalarm_conn):
    HOST='127.0.0.1'
    PORT = 62937
    BUFSIZE = 2048
    ADDR = (HOST, PORT)
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)

    while True:
        # print('alarm')
        global i
        cmd = '<alarm><req>yes</req></alarm>\n'  # 报警信息
        tcpCliSock.send(cmd.encode())
        xml_data = tcpCliSock.recv(BUFSIZE).decode('gb2312')
        alarm_data = {}
        n = 0
        flag = 1
        while flag and 16 < len(xml_data):
            data = dict()  # 可以动态建立字典，即不会覆盖之间数据，若用data1 = {}则覆盖
            if xml_data.find('<localtime>') != -1:
                data['time'] = xml_data[xml_data.find('<localtime>') + 11: xml_data.find('</localtime>')];
                # print('时间',data['localtime'])
            else:
                flag = 0
            if flag and xml_data.find('<no>') != -1 and xml_data.find('</localtime>') + 12 == xml_data.find('<no>'):
                data['num'] = xml_data[xml_data.find('<no>') + 4: xml_data.find('</no>')];
                # print('号',data['no'])
            else:
                flag = 0
            if flag and xml_data.find('<prio>') != -1 and xml_data.find('</no>') + 5 == xml_data.find('<prio>'):
                if int(xml_data[xml_data.find('<prio>') + 6: xml_data.find('</prio>')]) ==1:
                    data['prio'] ='提示'
                    data['priority'] = 0
                if int(xml_data[xml_data.find('<prio>') + 6: xml_data.find('</prio>')]) == 2:
                    data['prio'] = '警告'
                    data['priority'] = 1
                if int(xml_data[xml_data.find('<prio>') + 6: xml_data.find('</prio>')]) == 3:
                    data['prio'] = '暂停'
                    data['priority'] = 2
                if int(xml_data[xml_data.find('<prio>') + 6: xml_data.find('</prio>')]) == 4:
                    data['prio'] = '急停'
                    data['priority'] = 3
                # print('优先级',data['prio'])
            else:
                flag = 0
            if flag and xml_data.find('<v1>') != -1 and xml_data.find('</prio>') + 7 == xml_data.find('<v1>'):
                data['detail'] = xml_data[xml_data.find('<v1>') + 4: xml_data.find('</v1>')]
                # print('内容',data['v1'])

                alarm_data[n] = data
                n += 1
            i = xml_data.find('</tm>') + 13  # 跳转到下一行<alarm>。。。。。。。</alarm>
            xml_data = xml_data[i:]
        # if len(alarm_data)>0:
            # print(alarm_data)
        childalarm_conn.send([alarm_data])
        time.sleep(1)

    # tcpCliSock.close()

