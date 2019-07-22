# ---------------------普通函数实现---------------------------------->
# def line1(k, x, b):
# 	print('y = %d' % (k * x + b))
#
#
# line1(1, 100, 1)
# line1(1, 50, 1)
# ---------------------------闭包实现-------------------------------->


def line(k, b):
	def line_in(x):
		print('y = %d' % (k * x + b))

	return line_in


# l1 = line(1, 1)
# l1(100)
# l1(50)

l2 = line(2, 2)
l2(100)
l2(50)

"""
l1,l2一样的代码,一样的函数参数,结果不一样,因为他们的环境变量/自由变量不一样
闭包的概念:自由变量 + 内部函数

"""

"""了解:类的装饰器"""
