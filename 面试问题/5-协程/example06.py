# -*- coding: utf-8 -*-
import socket
import time


def nonblocking_way():
    """非阻塞"""
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(("example.com", 80))
    except BlockingIOError:
        # 非阻塞连接过程中也会抛出异常
        pass

    request = "GET /HTTP/1.0\r\nHost: example.com\r\n\r\n"
    data = request.encode("ascii")
    # 不知道socket何时就绪,所以不断尝试发送
    while True:
        try:
            sock.send(data)
            # 直到send不抛异常,则发送完成
            break
        except OSError:
            pass

    response = b""
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk += sock.recv(4096)
            break
        except OSError:
            pass
    return response


def sync_way():
    """同步非阻塞"""
    res = []
    for i in range(10):
        res.append(nonblocking_way())
    return len(res)


t1 = time.time()
sync_way()
t2 = time.time()
print(t2 - t1)
