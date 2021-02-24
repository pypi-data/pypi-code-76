#oding = utf-8
# -*- coding:utf-8 -*-
#oding = utf-8
# -*- coding:utf-8 -*-

from socket import *
from time import ctime, sleep
import threading


class ChatRoomPlus:
    def __init__(self):
        # 全局参数配置
        self.encoding = "utf-8"  # 使用的编码方式
        self.broadcastPort = 10100   # 广播端口
        self.myhost="A888-888-888-887"
        self.myport="3"
        # 创建广播接收器
        self.recvSocket = socket(AF_INET, SOCK_DGRAM)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.recvSocket.bind(('', self.broadcastPort))

        # 创建广播发送器
        self.sendSocket = socket(AF_INET, SOCK_DGRAM)
        self.sendSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # 其他
        self.threads = []

    def send(self, message, host, port):
        """发送广播"""
        sendData = str([message, f"{host}={port}"])
        self.sendSocket.sendto(sendData.encode(self.encoding), ('255.255.255.255', self.broadcastPort))

    def recv(self,host, port):
        """接收广播"""

        recvData = self.recvSocket.recvfrom(1024)[0].decode(self.encoding)
        print(recvData)
        if list(eval(recvData))[0].split("=")[0]==self.myhost:
            if list(eval(recvData))[0].split("=")[1]==self.myport:
                print(recvData)
                #print("【%s】[%s : %s] : %s" % (ctime(), recvData[1][0], recvData[1][1], recvData[0].decode(self.encoding)))

    def start(self):
        """启动线程"""
        t1 = threading.Thread(target=self.recv,args=(self.myhost,self.myport))
        t2 = threading.Thread(target=self.send,args=("helloworld","A888-888-888-888","3"))
        self.threads.append(t1)
        self.threads.append(t2)
        for t in self.threads:
            t.setDaemon(True)
            t.start()
        while True:
            pass


if __name__ == "__main__":
    demo = ChatRoomPlus()
    demo.start()