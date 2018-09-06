#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TCP Echo Server，多进程，阻塞 blocking I/O
import os
import socket
from multiprocessing import Process


def client_handler(client_sock, client_addr):
    '''接收各个客户端发来的数据，并原样返回'''
    try:
        while True:
            # 接收客户端发来的数据，阻塞，直到有数据到来
            # 如果客户端关闭了连接，data是空字符串
            data = client_sock.recv(4096)
            if data:
                print('Child Process [PID: {}], received {}({} bytes) from {}'.format(os.getpid(), data, len(data), client_addr))
                # 返回响应数据，将客户端发送来的数据原样返回
                client_sock.send(data)
                print('Child Process [PID: {}], sent {} to {}'.format(os.getpid(), data, client_addr))
            else:
                print('Child Process [PID: {}], client {} is closed'.format(os.getpid(), client_addr))
                break
    except:
        # 如果客户端强制关闭连接，会报异常: ConnectionResetError: [Errno 104] Connection reset by peer
        pass
    finally:
        # 关闭为这个客户端服务的socket
        client_sock.close()


# 创建监听socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket默认不支持地址复用，OSError: [Errno 98] Address already in use
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定IP地址和固定端口
server_address = ('', 9090)
print('TCP Server starting up on port {}'.format(server_address[1]))
server_sock.bind(server_address)

# socket默认是主动连接，调用listen()函数将socket变为被动连接，这样就可以接收客户端连接了
server_sock.listen(5)

try:
    while True:
        print('Main Process [PID: {}], waiting for client connection...'.format(os.getpid()))

        # 主进程只用来负责监听新的客户连接
        # client_sock是专为这个客户端服务的socket，client_addr是包含客户端IP和端口的元组
        client_sock, client_addr = server_sock.accept()
        print('Main Process [PID: {}], client {} is connected'.format(os.getpid(), client_addr))

        # 为每个新的客户连接创建一个子进程，用来处理客户数据
        client = Process(target=client_handler, args=(client_sock, client_addr))
        client.start()
        # 子进程已经复制了一份client_sock，所以主进程中可以关闭此client_sock
        client_sock.close()
finally:
    # 关闭监听socket，不再响应其它客户端连接
    server_sock.close()
