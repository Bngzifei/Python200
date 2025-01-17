# select与epoll、apache与nginx实现原理对比

## 关于select 与epoll

两种IO模型,都属于多路IO就绪通知,提供了对大量文件描述符就绪检查的高性能方案,只不过实现方式有所不同:

### select:

一个select()系统调用来监视包含多个文件描述符的数组,当seletc返回,该数组中就绪的文件描述符便会被内核修改标志位。

select的跨平台做的很好,几乎每个平台都支持。

select缺点有以下三点:

1. 单个进程能够监视的文件描述符的数量存在最大限制
2. select()所维护的存储大量文件描述符的数据结构,随着文件描述符数量的增长,其在用户态和内核的地址空间的复制所引发的开销也会线性增长。
3. 由于网络响应时间的延迟使得大量TCP连接处于非活跃状态，但调用select()还是会对所有的socket进行一次线性扫描,会造成一定的开销。

### poll:

poll是unix沿用select自己重新实现了一遍,唯一解决的问题是poll没有最大文件描述符数量的限制.

### epoll:

epoll带来了两个优势,大幅度提升了性能。

1. 基于事件的就绪通知方式，select/poll方式,进程只有在调用一定的方法后,内核才会对所有监视的文件描述符进行扫描,而epoll事件通过epoll_ctl()注册一个文件描述符,一旦某个描述符就绪时,内核会采用类似callback的回调机制,迅速激活这个文件描述符,epoll_wait()便会得到通知。
2. 调用一次epoll_wait()获得就绪文件描述符时,返回的并不是实际的描述符,而是一个代表就绪描述符数量的值,拿到这些值去epoll指定的一个数组中依次取得相应数量的文件描述符即可,这里使用内存映射(mmap)技术,避免了复制大量文件描述符带来的开销。

当然epoll也有一定的局限性,epoll只有Linux2.6才有实现,而其他平台没有,这和apacha这种优秀的跨平台服务器,显然是有些背道而驰了。

## 文件描述符

文件描述符时操作系统资源,用于表示连接、打开的文件，以及其他信息。Nginx每个连接可以使用两个文件描述符。例如，如果Nginx充当代理时，通常一个文件描述符表示客户端连接，另一个连接到代理服务器。如果开启了HTTP保持连接，这个比例会更低。对于有大量连接服务的系统，下面的设置可能需要调整一下：

- sys.fs.file_max——文件描述符系统级别的限制
- nofile——用户级别文件描述符限制，在/etc/security/limits.conf文件中修改。

## 临时端口

当Nginx充当代理时候,每个到上游服务器的连接都使用一个短暂或临时端口。可能需要修改这些设置：

- net.ipv4.ip_local_port_range —— 端口值的起止范围。如果你发现用尽端口号，可以增大端口范围。一般端口号设置是1024到65000。

## 调优Nginx配置

以下是一些可以影响性能的Nginx指令。如上所述，我们只讨论自己能调整的指令。

- worker_processes——Nginx工作进程数(默认值是1),在大多数情况下,一个CPU内核运行一个工作进程最好,建议将这个指令设置成自动就可以。有时可能想增大这个值，比如当工作进程需要做大量的磁盘I/O。
- worker_connections——每个工作进程可以处理并发的最大连接数。默认值是512,但多数系统有充足的资源可以支撑更多的连接.合适的设置可以根据服务器的大小和流量的性质决定,可以通过测试修改.

## 长连接

长连接对性能有很大的影响,通过减少CPU和网络开销需要开启或关闭连接.Nginx终止所有客户端连接,创建到上游服务器独立的连接.Nginx支持客户端和上游服务器两种长连接.下面是和客户端的长连接相关的指令:

- keepalive_requests-单个客户端长连接可以请求的数量,默认值是100,但是当使用压力测试工具从一个客户端发送多个请求测试时,这个值设更高些特别有用.
- keepalive_timeout-空闲长连接保持打开状态的时间.

下面是和上游服务器长连接的相关指令:

- keepalive-每个工作进程中空闲长连接到上游服务器保持开启的连接数量.没有默认值

要使用连接到上游服务器的长连接,必须要配置文件中下面的指令.

```nginx
proxy_http_version 1.1;
proxy_set_header Connection "";
```

## 访问日志

记录每个请求会消耗CPU和I/O周期,一种降低这种影响的方式是缓冲访问日志.使用缓冲,而不是每条日志记录都单独执行写操作,Nginx会缓冲一连串的日志记录,使用单个操作把它们一起写到文件中.

要启用访问日志的缓存,就涉及到在access_log指令中buffer=size这个参数.当缓存区达到size值时,Nginx会把缓存区的内容写到日志中.让Nginx在指定的一段时间后写缓存,就包含flush=time参数.当两个参数都设置了,当下个日志条目超出缓存区值或者缓冲区中日志条目存留时间超过设定的时间值,Nginx都会将条目写入日志文件.当工作进程重新打开它的日志文件或退出时,也会记录下来.要完全禁用访问日志记录的功能,将access_log指令设置成off参数.

## Sendfile

操作系统的sendfile()系统调用可以实现从一个文件描述符到另一个文件描述符的数据拷贝,通常实现零拷贝,这能加速TCP数据传输.要让Nginx使用它,在http或server或location环境中包含sendfile指令.Nginx可以不需要切换到用户态,就把缓存或磁盘上的内容写入套接字.而且写的速度非常快.消耗更少的CPU周期.注意,尽管使用sendfile()数据拷贝可以绕过用户态,这不适用于常规的Nginx处理改变内容的链和过滤器,比如gzip.当配置环境下有sendfile指令和激活内容更改过滤器指令时,Nginx会自动禁用sendfile.

## 限制

你可以设置多个限制,防止用户消耗太多的资源,避免影响系统性能和用户体验及安全.以下是相关的指令:

- limit_conn and limit_conn_zone ----Nginx接受客户连接的数量限制,例如单个IP地址的连接.设置这些指令可以防止单个用户打开太多的连接,消耗超出自己的资源.
- limit_rate-传输到客户端响应速度的限制(每个打开多个连接的客户消耗更多的带宽).设置这个限制防止系统过载,确保所有客户端更均匀的服务质量.
- limit_req and limit_req_zone ----Nginx处理请求的速度限制,与limit_rate有相同的功能.可以提高安全性,尤其是对登录页面,通过对用户限制请求速率设置一个合理的值,避免太慢的程序覆盖你的应用请求.
- max_conns上游配置块中服务器指令参数。在上游服务器组中单个服务器可接受最大并发数量。使用这个限制防止上游服务器过载。设置值为0（默认值）表示没有限制。
- queue(NGINX Plus)--创建一个队列,用来存放在上游服务器中超出他们最大max_cons限制数量的请求.这个指令可以设置队列请求的最大值,还可以选择设置在错误返回之前最大等待时间(默认值是60秒).如果忽略这个指令,请求不会放入队列.

## 缓存和压缩可以提高性能

NGINX的一些额外功能可用于提高web应用的性能,调优的时候web应用不需要关掉,但值得一提,因为它们的影响可能很重要.它们包括缓存和压缩.

### 缓存

一个启用NGINX缓存的情景,一组web或者应用服务器负载均衡,可以显著缩短对客户端的响应时间,同时大幅度降低后端服务器的负载.缓存本身就可以作个专题来讲,这里我们就不试图讲它了,参阅NGINX Plus管理手册的NGINX的内容缓存.

### 压缩

所以使用更小的网络带宽.然而尽管压缩数据会消耗CPU资源,但当需要减少网络带宽使用时这样做非常有效.需要注意的是,不能对已压缩的文件再压缩,例如JPEG文件.有关更多的信息,请参阅 NGINX Plus管理指南中的压缩和解压缩.







