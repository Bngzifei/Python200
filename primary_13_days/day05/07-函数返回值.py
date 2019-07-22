print('返回值:')

"""返回值:"""

"""
当执行完函数之后,如果想要把函数的执行结束后的结果返回给函数的调用者(即函数执行完的某一结果,函数外部执行的时候是否需要),
就可以给函数添加返回值
默认所有的函数都是没有返回值
-> None 
无绝对的要求,看需求写return
所有的编程语言中都有.都是返回函数的执行结果
没有设置返回值,则返回None
关键字:return
函数外部使用函数内部数据用return
函数内部使用外部数据用参数

多写多练,才能熟练
前期就是掌握概念,理解
"""


def func_sum(a, b):
	result = a + b
	return result  # return 关键字,只能在函数内部使用


re = func_sum(1, 3)  # 返回Any,即可以返回任意的数据类型(可以是一个整数,小数,字符串,列表,元组,字典,集合等等)
print(re)
# print(func_sum(1, 3))  # 输出函数的返回值
#
# print(func_sum)  # 输出函数的地址 <function func_sum at 0x0000024DB34D2E18>,加了()就是调用函数,不加()就是函数名,函数名代表了一个函数在内存里面的地址
