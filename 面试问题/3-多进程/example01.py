# -*- coding: utf-8 -*-
import multiprocessing


def f(q):
    print("(%s) 进程开始放入数据..." % multiprocessing.current_process().pid)
    q.put("Python")


if __name__ == '__main__':
    # 创建进程通信的Queue
    q = multiprocessing.Queue()
    # 创建子进程
    p = multiprocessing.Process(target=f, args=(q,))
    # 启动子进程
    p.start()
    print("(%s) 进程开始取出数据..." % multiprocessing.current_process().pid)
    # 队列对象取出数据
    print(q.get())
    p.join()
