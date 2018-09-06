#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TCP Echo Server，单进程，阻塞 blocking I/O
import socket


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
        print('Main Process, waiting for client connection...')

        # client_sock是专为这个客户端服务的socket，client_addr是包含客户端IP和端口的元组
        client_sock, client_addr = server_sock.accept()
        print('Client {} is connected'.format(client_addr))

        try:
            while True:
                # 接收客户端发来的数据，阻塞，直到有数据到来
                # 事实上，除非当前客户端关闭后，才会跳转到外层的while循环，即一次只能服务一个客户
                # 如果客户端关闭了连接，data是空字符串
                data = client_sock.recv(4096)
                if data:
                    print('Received {}({} bytes) from {}'.format(data, len(data), client_addr))
                    # 返回响应数据，将客户端发送来的数据原样返回
                    client_sock.send(data)
                    print('Sent {} to {}'.format(data, client_addr))
                else:
                    print('Client {} is closed'.format(client_addr))
                    break
        finally:
            # 关闭为这个客户端服务的socket
            client_sock.close()
finally:
    # 关闭监听socket，不再响应其它客户端连接
    server_sock.close()
