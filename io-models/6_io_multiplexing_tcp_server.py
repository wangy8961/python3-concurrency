#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import selectors
import socket

# 自动选择当前OS中最优的I/O multiplexing接口，Linux中会使用selectors.EpollSelector
sel = selectors.DefaultSelector()


def accept(sock, mask):
    '''监听套接字创建新的客户端连接'''
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)  # 将新的客户端socket注册到epoll实例上，并监听读事件


def read(conn, mask):
    '''接收客户端数据，并原样返回'''
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


sock = socket.socket()
sock.bind(('', 9090))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
