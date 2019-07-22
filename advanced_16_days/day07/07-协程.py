"""
还是单任务(单线程程序),只是在遇到阻塞(就是等待)的时候,切换任务去执行
协程:微线程/用户级别的多任务机制.<用户自己的程序实现的>
线程/进程:操作系统级别的多任务机制

使用场景:
多任务数量很大>几千的时候就使用协程  或者网络型的程序  优先考虑使用协程

挂起:就是在那个位置定住了不动,等到下一次开始的时候从这个位置继续开始执行.

"""
import time


def worker1():
	"""生成器函数"""
	while True:
		print('in worker1')
		yield
		time.sleep(0.5)


def worker2():
	while True:
		print('in worker2')
		yield
		time.sleep(0.5)


if __name__ == '__main__':
	# 执行生成器对象的代码:1.创建生成器对象  2.next(生成器对象)
	# 创建
	w1 = worker1()  # 只有这个是不行的,需要next()调用才能把这个生成器函数运行起来
	w2 = worker2()
	while True:  # 交替执行,并发
		# 调用next()函数
		next(w1)
		next(w2)

"""
bug:臭虫,debug:就是杀死臭虫的意思

F8:步过.跳过调用的部分  可以多处打断点,在断点的地方进行调试.
F7:步进,进入调用函数的部分

"""