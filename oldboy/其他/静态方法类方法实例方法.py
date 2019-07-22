# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2019-05-08 09:22:33
# @Last Modified by:   Marte
# @Last Modified time: 2019-05-09 15:52:24


# 静态方法:

    #定义：使用装饰器@staticmethod。参数随意，没有“self”和“cls”参数，但是方法体中(就是在方法中不能出现类中的属性和方法)不能使用类或实例的任何属性和方法；

    # 调用：实例对象和类对象都可以调用

import time

class TimeTest(object):
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    # 静态方法是类中的函数,不需要实例.静态方法主要是 用来存放逻辑性的代码,逻辑上属于类,但是和类本身没有关系,也就是说在静态方法中,不会涉及到类中的方法和属性的操作.
    # 可以理解为,静态方法是一个 独立的, 单纯的函数 ,它仅仅 托管于 某个类的名称空间中,便于维护和使用
    # 如下,使用了静态方法(函数),然而方法体中并没有使用(也不能使用)类或者实例的属性(或方法).如果要获得当前时间的字符串的时,并不一定要实例化对象,此时对于静态方法而言,所在的类更像是一种名称空间.
    @staticmethod
    def showTime():
        return time.strftime("%H:%M:%S", time.localtime())

# 其实,我们也可以在类外面写一个同样的函数来 做这些事,但是这样做就打乱了逻辑关系,也会导致后续代码维护困难.

# 当前类也可以直接调用静态方法
print(TimeTest.showTime())


# 在下面的TimeTest(初始化时候的三个参数)中,只要是出现 调用的时候  类(实例化一个对象的参数,就是___init__方法中的参数)  这样的就是调用.  如果是  在定义一个类的时候,  class  A(继承的父类,上一级类是啥):
# 这样的就是定义一个类
#
# 先创建一个,或者说实例化一个实例对象
t = TimeTest(2, 10, 10)
# 实例对象调用静态方法
nowTime = t.showTime()
print(nowTime)




# 类方法:

    # 定义：使用装饰器@classmethod。第一个参数必须是当前类对象，该参数名一般约定为“cls”，通过它来传递类的属性和方法（不能传实例的属性和方法）；

    # 调用：实例对象和类对象都可以调用。


# 原则上,类方法是将类本身作为对象进行操作的方法.假设有个方法,且这个方法在逻辑上采用类本身作为对象来调用更合理,那么这个方法就可以定义为类方法.另外,如果需要继承,也可以定义为类方法.
#

# 如下场景：

# 假设我有一个学生类和一个班级类，想要实现的功能为：
    # 执行班级人数增加的操作、获得班级的总人数；
    # 学生类继承自班级类，每实例化一个学生，班级人数都能增加；
    # 最后，我想定义一些学生，获得班级中的总人数。

# 思考：这个问题用类方法做比较合适，为什么？因为我实例化的是学生，但是如果我从学生这一个实例中获得班级总人数，在逻辑上显然是不合理的。同时，如果想要获得班级总人数，如果生成一个班级的实例也是没有必要的。
#
#
class ClassTest(object):
    # 定义类属性
    __num = 0

    @classmethod
    def addNum(cls):
        """增加个数"""
        cls.__num += 1

    @classmethod
    def getNum(cls):
        """获取个数"""
        return cls.__num

    # 这里我用到魔法方法 __new__，主要是为了在创建实例的时候调用人数累加的函数。
    def __new__(self):
        # 调用类方法 增加个数
        ClassTest.addNum()
        return super(ClassTest, self).__new__(self)


class Student(ClassTest):
    def __init__(self):
        self.name = ''

a = Student()
b = Student()
c = Student()
d = Student()
print(ClassTest.getNum())

# 1.)静态方法常驻内存,实例方法不是,所以'静态方法效率高,但是占内存'
# 事实上,方法都是一样的,在加载的时机和占用内存上,静态方法和实例方法是一样的,在类型第一次被使用时加载.
# 调用的速度上基本没有差别
# 2.)静态方法在堆上分配内存,实例方法在栈上,事实上所有的方法都不可能在堆或者栈上分配内存,方法作为代码是被加载到
# 特殊的代码内存区域,这个区域是不可以写的
# 3.)实例方法需要先创建实例才可以调用
# 4.)静态方法是静态绑定到子类,不是被继承
# 5.)一般使用频繁的方法是用静态方法,用的少的用动态的,静态的速度快,占内存,动态的稍微速度慢点,但是调用完之后,立即释放类,可以节省内存,可以根据自己的需要选择是动态方法还是静态方法
# 6.)静态方法修改的是类的状态,而对象修改的是各个对象的状态
# 7.)类的实例调用是在类的生命周期中存在,当类没有了之后,对应的实例也就没有了.对应的实例也就没有了,对应的方法也就没有了.
# 静态方法则不然,只要你引用了那个静态来当命名空间,它就会一直存在,直到我们退出系统
# 8.)类方法只要创建了,运行就会生成内存,并且可以直接调用 类名 + 方法,名 就可以,而实例方法则是调用的时候才会生成内存
# 9.)静态方法在程序开始时生成内存,实例方法在程序运行时生成内存,所以静态方法可以直接调用,实例方法需要先生成实例,通过实例
# 来调用方法.静态方法速度更快,但是多了会占用内存
# 10.)静态方法是连续的,因为是在程序开始的时候就生成了,而实例申请的是离散空间









