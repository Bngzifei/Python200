print('参数:')
"""函数:参数"""

"""
()里面就是参数
作用:目的就是为了给真实的数据进行占位.(和占位符%类似)
位置要一一对应(有顺序要求)
把外部数据传入内部
参数就是一个媒人(中介.桥梁)的作用
优点:增加函数的通用性,灵活性
参数类似变量
可以有参数,也可以没有
有几个,就要放几个
是否需要使用外部的数据(是,就使用参数.不是,不加参数),即外部的数据是否需要进入这个函数内部进行运算执行
参数的使用取决于:函数内部是否需要使用函数外部的数据

定义函数时的参数叫形参,为真实数据占位,在调用函数时写的参数叫实参.
实参会传递给形参
形参:占位,传值作用
"""


def func_sum(num1, num2):  # 在定义函数时如果给函数添加了参数那么调用函数的时候,一定要给它传递真实的参数(即有形参一定要有实参)
	"""任意两个个数字求和"""
	result = num1 + num2
	print(result)


# parameter:参数,unfilled:没有被填充
# func_sum()  # TypeError: func_sum() missing 2 required positional arguments: 'num1' and 'num2'
func_sum(10, 30)
