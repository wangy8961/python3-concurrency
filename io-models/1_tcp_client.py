#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from datetime import datetime
import socket


server_ip = input('Please enter the TCP server ip: ')
server_port = int(input('Enter the TCP server port: '))
client_num = int(input('Enter the TCP clients count: '))

# 保存所有已成功连接的客户端TCP socket
client_socks = []

for i in range(client_num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    client_socks.append(sock)
    print('Client {}[ID: {}] has connected to {}'.format(sock, i, (server_ip, server_port)))

while True:
    for s in client_socks:
        data = str(datetime.now()).encode('utf-8')
        s.send(data)
        print('Client {} has sent {} to {}'.format(s, data, (server_ip, server_port)))
    # 睡眠3秒后，继续让每个客户端连接向TCP Server发送数据
    time.sleep(3)
