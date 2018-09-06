#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TCP Echo Server，单进程，非阻塞 nonblocking I/O
import socket


# 用来保存所有已成功连接的客户端，每个列表元素是client_sock和client_addr组成的元组
clients = []

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

# 将监听用的server_sock设置为非阻塞
server_sock.setblocking(False)

print('Main Process, waiting for client connection...')

try:
    while True:
        try:
            # client_sock是专为这个客户端服务的socket，client_addr是包含客户端IP和端口的元组
            client_sock, client_addr = server_sock.accept()
        except:
            # server_sock设置为非堵塞后，如果accept时，恰巧没有客户端connect，那么accept会产生一个异常
            pass
        else:
            print('Client {} is connected'.format(client_addr))
            # 将新的客户端连接socket也设置为非阻塞
            client_sock.setblocking(False)
            # 添加到client_socks列表中
            clients.append((client_sock, client_addr))

        # 循环处理每个客户端连接
        for client_sock, client_addr in clients:
            try:
                data = client_sock.recv(4096)
                if data:
                    print('Received {}({} bytes) from {}'.format(data, len(data), client_addr))
                    # 返回响应数据，将客户端发送来的数据原样返回
                    client_sock.send(data)
                    print('Sent {} to {}'.format(data, client_addr))
                else:
                    print('Client {} is closed'.format(client_addr))
                    # 关闭为这个客户端服务的socket
                    client_sock.close()
                    # 从列表中删除
                    clients.remove((client_sock, client_addr))
            except:
                # client_sock设置为非堵塞后，如果recv时，恰巧客户端没有发送数据过来，将会产生一个异常
                pass
finally:
    # 关闭监听socket，不再响应其它客户端连接
    server_sock.close()
