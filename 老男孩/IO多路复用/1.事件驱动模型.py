"""
问题:遇到IO操作就切换
但是,什么时候切回去了?怎么确定IO操作完了呢?
传统的编程是如下线性模式的:
	开始-->代码块A-->代码块B-->代码块C-->代码块D-->..结束
	每一个代码块里是完成各种各样事情的代码.但编程者需要知道代码块A,B,C,D的执行顺序.唯一能够改变这个流程的数据.输入不同的数据,根据条件语句判断.流程或许就改为A-->C-->E..-->结束.每一次程序运行顺序或许很不同,但它的控制流程是由输入数据和你编写的程序决定的.如果你知道这个程序当前的运行状态(包括输入数据和程序本身),那你就知道接下来甚至一直到它结束的运行流程.

对于事件驱动型程序模型,它的流程大致如下:
	开始->初始化-->等等
与上面传统的模式不同,事件驱动程序在启动之后,就在那里等待,等待什么呢?等待事件被触发.传统编程下也有'等待'的时候,比如你在代码块D中,你定义了一个input(),需要用户输入数据.但这与下面的等待不同,传统编程的"等待",比如"input()",你作为程序编写者是知道或者强制用户输入某个东西的,或许是数字,或许是文件名称,如果用户输入错误,你还需要提醒他,并请他重新输入.事件驱动程序的等待则是完全不知道,也不强制用户输入或者干什么.只要某一事件发生,那么程序就会做出相应的"反应",这些事件包括:输入信息,鼠标,敲击键盘上的某个键还有系统内部定时器触发.

UI编程都是这种思想.以后工作的时候也基本是这种思想.

事件驱动编程思想:一种编程范式.就是一种写代码的思路
"""
# while True:
# 	# 检测click什么时候发生.
# 	pass  # 死循环的时候就是把cpu一直占用.极大的浪费cpu
"""
创建一个线程循环检测是否有鼠标点击:
那么这个方式有以下几个缺点:
	1.>CPU资源浪费,可能鼠标点击的频率非常小,但是扫描线程还是会一直循环检测,这会造成很多CPU资源浪费,如果扫描鼠标点击的接口是阻塞的呢?
	2.>如果是阻塞的,又会出现下面这样的问题,如果我们不但要扫描鼠标点击,还要扫描键盘是否按下,由于扫描鼠标时鼠标被阻塞了,那么可能永远不会去扫描键盘
	3.>如果一个循环需要扫描的设备非常多,这又会引来响应时间的问题
	所以,该方式是非常不好的.
"""
# -------------------------事件驱动模型--------------->
"""
目前大部分的UI编程都是事件驱动模型,如很多UI平台都会提供onClick()事件,这个事件就代表鼠标按下事件.事件驱动模型思路如下:
1.>有一个事件<消息>队列
2.>鼠标按下时,往这个队列中增加一个点击事件<消息>
3.>有个循环,不断从队列取出事件,根据不同的事件,调用不同的函数,如onClick(),
onKeyDown()等
4.>事件<消息>一般都各自保存各自的处理函数指针,这样,每个消息都有独立的处理函数.

事件队列:放事件的队列
事件驱动编程是一种编程范式,这里程序的执行是由外部事件来决定.它的特点是包含一个事件循环,当外部事件发生时使用回调机制来触发相应的处理.
另外两种常见的编程范式是单线程同步以及多线程编程

理解:就是之前项目中使用一个字典类实现一个动作对应一个函数的关系.

谁在监测鼠标的点击:操作系统
问到谁在和硬件打交道的时候,一定是操作系统.
"""
# -----------------------IO模型准备-------------------------->
"""
协程实现IO阻塞自动切换,那么协程又是怎么实现的,在原理上如何实现?如何去实现事件驱动的情况下IO的自动阻塞的切换,这个专业名词叫什么?-->IO多路复用
比如socketserver,多个客户端连接,单线程下实现并发效果,就叫多路复用

同步IO和异步IO,阻塞IO和非阻塞IO分别是什么?到低有什么区别?不同的人在不同的上下文给出的答案是不同的,所以先限定一下本文的上下文.
本文讨论的背景是linux环境下的networkIO

"""

"""
1.>用户空间和内核空间:
	现在操作系统都是采用虚拟存储器,那么对32位操作系统而言,它的寻址空间为4G<2的32次方>
操作系统的核心是内核,独立于普通的应用程序,可以访问受保护的内存空间,也有访问底层硬件设备的所有权限.为了保证用户进程不能直接操作内核,保证内核的安全,操作系统将虚拟空间分为两部分,一部分为内核空间,一部分为用户空间.针对linux操作系统而言,将最高的16字节,供内核使用,称为内核空间,而将较低的36字节,供各个进程使用,称为用户空间.

2.>进程切换:
	为了控制进程的执行,内核必须有能力挂起正在cpu上运行的进程,并恢复以前挂起的某个进程的执行.这种行为被称为进程切换.这种切换是由操作系统来完成的.因此可以说,任何进程都是在操作系统的内核的支持下运行的,是与内核紧密相关的.
	从一个进程的运行转到另一个进程上运行,这个过程中经过下面这些变化:
		保存处理机上下文,包括程序计数器和其他寄存器.
		更新PCB信息
		把进程的PCB移入相应的队列,如就绪,在某事件阻塞等队列
		选择另一个进程执行,并更新其PCB
		更新内存管理的数据结构
		恢复处理机上下文
	注:切换进程总而言之就是很耗资源的.
	
3.>进程阻塞:
	正在执行的进程,由于期待的某些事件未发生,如请求系统资源失败,等待某种操作的完成,新数据尚未到达或无新工作做等,则由系统自动执行阻塞原语<Block>,使自己由运行状态变为阻塞状态,可见,进程的阻塞是进程自身的一种主动行为,也因此只有处于运行态的进程(获得cpu),才可能将其转为阻塞状态.当进程进入阻塞状态,是不占用cpu资源的.

4.>文件描述符fd:
	文件描述符<file descriptor>是计算机科学中的一个术语,是一个用于表述指向文件的引用的抽象化概念.
	文件描述符在形式上是一个非负整数.实际上,它是一个索引值,指向内核为每一个进程所维护的该进程的打开文件的记录表.当程序打开一个现有文件或则创建一个新文件时,内核向进程返回一个文件描述符.在程序设计中,一些涉及底层的程序编写往往会围绕着文件描述符展开,但是文件描述符这一概念往往只适用于unix,linux这样的操作系统.

5.>缓存I/O:
	缓存I/O又被称作标准I/O,大多数文件系统的默认I/O操作都是缓存I/O.在Linux的缓存I/O机制中,操作系统会将I/O的数据缓存在文件的页缓存<page cache>中,也就是说,数据会先被拷贝到操作系统内核的缓存区中,然后才会从操作系统内核的缓存区拷贝到应用程序的地址空间.用户空间没法直接访问内核空间.内核态到用户态的数据拷贝
思考:为啥数据一定要先到内核区,直接到用户内存不是更直接吗?
答:数据在传输过程中需要在应用程序地址空间和内核进行多次数据拷贝操作,这些数据拷贝操作所带来的cpu以及内存开销是非常大的.

6.>同步<synchronous>IO和异步<asynchronous>IO,阻塞<blocking>IO和非阻塞<non-blocking>IO分别是什么?,到低有什么区别?这个问题其实不同的人给出的答案都可能不同,比如wiki,就认为异步IO和非阻塞IO是一个东西.这其实是因为不同的人知识背景不同,并且在讨论这个问题的时候上下文也不同,所以,本文讨论的背景是Linux环境下的network IO

注意:能够和硬件发生数据交互的一定是操作系统.
"""
# ---------------------缓存IO-------------------------->
"""
1.>阻塞IO:在linux中默认情况下所有的socket都是blocking,一个典型的读操作流程大致是这样:
	当用户进程调用了recvfrom这个系统调用,内核就开始了IO的第一个阶段:准备数据.对于network io 来说,很多时候数据在一开始还没有到达,比如,还没有收到一个udp包,这个时候内核就要等待足够的数据到来.而在用户进程这边,整个进程会被阻塞.当内核一直等到数据准备好了,它就会将数据从内核中拷贝到用户内存,然后内核返回结果,用户进程才解除block的状态,重新运行起来.
	所以,阻塞IO的特点就是在IO执行的两个阶段都被block了.
	
2.>非阻塞IO:linux下,可以通过设置socket使其变为non-blockingIO
发太多的系统调用,数据没有被及时的处理.数据不及时

3.>IO多路复用:
	IO多路复用,select,epoll .有些地方也称这种IO方式为event driven IO.我们都知道,select/epoll 的好处就在于单个process就可以同时处理多个网络连接的IO,它的基本原理是select/epoll这个功能会不断的轮询所负责的所有socket,当某个socket有数据到达了,就通知用户进程.
	当用户进程调用了select,那么整个进程会被block,内核会监视所有select所负责的socket,当任何一个socket中的数据准备好了,select就会返回.这个时候用户进程再调用read操作.将数据从内核拷贝到用户进程.

select 就是一个函数 在用户看来 看是否有人连接.如果没有,一直监听

recvfrom 又一次系统调用

https://pan.baidu.com/s/1kpmWHJqRUANN552PQgjmNw

函数的签名（方法签名）是用来定义一个函数(或方法)传入参数的类型，顺序和数量的，函数签名经常被用在函数重载，因为调用重载的方法从名字上

是无法确定你调用的是哪一个方法，而要从你传入的参数和该函数的签名来进行匹配，这样才可以确定你调用的是哪一个函数。
"""
