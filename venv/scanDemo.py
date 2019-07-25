import socket
import os
import re
import threading
import gevent
from multiprocessing import Process, Manager

#ip地址池
lists = []
lists1 = []
lists2 = []
lists3 = []
lists4 = []
lists5 = []
lists6 = []
lists7 = []
lists8 = []
lists9 = []
lists10 = []



total_ports = []
closed_ports = []
open_ports = {}
common_list = False
udp_scan = False
error = []
attack_ip = []


#获取IP列表
def getIP():
    ipLists = []

    # content = os.popen("ipconfig").read()
    content = "192.168.1.151"

    #匹配IP地址的正则表达式
    c = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", content)
    for i in c:
        if "255" not in i:
            # print(i)
            a = i.split('.')
            iptmp =a[0] + "." + a[1] + "." + a[2]
            for num in range(1,255):
                # print(num)
                ip = iptmp  + "." + str(num)
                # print (ip)
                if str(num) != a[3]:
                    ipLists.append(ip)
                    # print(ip)
    lists = list(set(ipLists))
    # return lists
    index = 0
    for ip in lists:
        # index += 1

        #10份
        # if (index % 10 == 0):
        #     lists1.append(ip)
        # elif (index % 10 == 1):
        #     lists2.append(ip)
        # elif (index % 10 == 2):
        #     lists3.append(ip)
        # elif (index % 10 == 3):
        #     lists4.append(ip)
        # elif (index % 10 == 4):
        #     lists5.append(ip)
        # elif (index % 10 == 5):
        #     lists6.append(ip)
        # elif (index % 10 == 6):
        #     lists7.append(ip)
        # elif (index % 10 == 7):
        #     lists8.append(ip)
        # elif (index % 10 == 8):
        #     lists9.append(ip)
        # elif (index % 10 == 9):
        #     lists10.append(ip)

        #1份
        lists1.append(ip)

def scan(lists):
    for ip in lists:
        check_port(ip, 445)

def check_port(ip, port, iplists):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((ip, port))
    except KeyboardInterrupt:
        print ("\nYou pressed Ctrl+C, Stopping Program.\n")
        error.append("\nYou pressed Ctrl+C, Stopping Program.\n")
        exit()
    except socket.gaierror as e:
        print ('Hostname could not be resolved.\nCheck if host is really up. Exiting..\n', e)
        error.append('Hostname could not be resolved.\nCheck if host is really up. Exiting..\n')
        exit()
    except socket.error as e:
        print ("Couldn't connect to server\n")
        error.append("Couldn't connect to server\n")
        exit()
    except Exception as e:
        print ("Unknown error occured", e)
        error.append("Unknown error occured")
        exit()
    if result == 0:
        open_ports[port] = 'open'
        total_ports.append(port)
        # print(ip)
        iplists.append(ip)
    elif result == 10061:
        closed_ports.append(port)
        total_ports.append(port)
    elif result == 10035:
        open_ports[port] = 'filtered'
        total_ports.append(port)
    sock.close()

#多线程进行扫描
def thread_scan():
    t1 = threading.Thread(target=scan, args=(lists1,))
    t1.start()

    t2 = threading.Thread(target=scan, args=(lists2,))
    t2.start()

    t3 = threading.Thread(target=scan, args=(lists3,))
    t3.start()

    t4 = threading.Thread(target=scan, args=(lists4,))
    t4.start()

    t5 = threading.Thread(target=scan, args=(lists5,))
    t5.start()

    t6 = threading.Thread(target=scan, args=(lists6,))
    t6.start()

    t7 = threading.Thread(target=scan, args=(lists7,))
    t7.start()

    t8 = threading.Thread(target=scan, args=(lists8,))
    t8.start()

    t9 = threading.Thread(target=scan, args=(lists9,))
    t9.start()

    t10 = threading.Thread(target=scan, args=(lists10,))
    t10.start()

#多进程
def process_scan(listt, iplists):
    p1 = Process(target=check_port, args=(listt,445,iplists,))
    p1.start()
    # p2 = Process(target=scan, args=(lists2,))
    # p2.start()

#协程扫描
def gevent_scan(lists):
    iplists = Manager().list([])  # 目标IP地址
    g_l = [gevent.spawn(process_scan, l, iplists) for l in lists]
    gevent.joinall(g_l)
    for ip in iplists:
        attack_ip.append(ip)

if __name__ == '__main__':
    # check_port('192.168.1.146', 445)
    getIP()
    # for i in lists:
    #     # print(i)
    #     check_port(i, 445)
    # for i in attack_ip:
    #     print(i)

    gevent_scan(lists1)

    for ip in attack_ip:
        print(ip)
    # p1 = Process(target=gevent_scan, args=(lists1,))
    # p2 = Process(target=gevent_scan, args=(lists2,))
    # p3 = Process(target=gevent_scan, args=(lists3,))
    # p1.start()
    # p2.start()
    # p3.start()
    # process_scan()





