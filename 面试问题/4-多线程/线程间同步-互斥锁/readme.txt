﻿通过互斥机制防止多个线程同时访问公共资源
互斥锁同步
上面的例子引出了多线程编程的最常见问题：数据共享。当多个线程都修改某一个共享数据的时候，需要进行同步控制。

线程同步能够保证多个线程安全访问竞争资源，最简单的同步机制是引入互斥锁。互斥锁为资源引入一个状态：锁定/非锁定。
某个线程要更改共享数据时，先将其锁定，此时资源的状态为“锁定”，其他线程不能更改；直到该线程释放资源，将资源的状态变成“非锁定”，
其他的线程才能再次锁定该资源。互斥锁保证了每次只有一个线程进行写入操作，从而保证了多线程情况下数据的正确性。

threading模块中定义了Lock类，可以方便的处理锁定：

#创建锁
mutex = threading.Lock()
#锁定
mutex.acquire([timeout])
#释放
mutex.release()

其中，锁定方法acquire可以有一个超时时间的可选参数timeout。如果设定了timeout，
则在超时后通过返回值可以判断是否得到了锁，从而可以进行一些其他的处理。

同步阻塞
当一个线程调用锁的acquire()方法获得锁时，锁就进入“locked”状态。每次只有一个线程可以获得锁。
如果此时另一个线程试图获得这个锁，该线程就会变为“blocked”状态，称为“同步阻塞”（参见多线程的基本概念）。

直到拥有锁的线程调用锁的release()方法释放锁之后，锁进入“unlocked”状态。
线程调度程序从处于同步阻塞状态的线程中选择一个来获得锁，并使得该线程进入运行（running）状态。

可重入锁:
http://c.biancheng.net/view/2617.html
为了支持在同一线程中多次请求同一资源，python提供了“可重入锁”：threading.RLock。
RLock内部维护着一个Lock和一个counter变量，counter记录了acquire的次数，从而使得资源可以被多次require。
直到一个线程所有的acquire都被release，其他的线程才能获得资源。这里以例1为例，如果使用RLock代替Lock，
则不会发生死锁。
https://www.cnblogs.com/amengduo/p/9586514.html
