print('------')
# ---------------如何对查询命令进行优化------------->
"""
1.>尽量避免全表扫描,首先考虑在where 以及 order by涉及的字段上建立索引
2.>尽量避免在where子句中对字段进行null判空操作.避免使用!=操作符,避免使用
or连接条件,或在where子句中对字段使用参数,对字段进行表达式或函数操作.否则
会导致全表扫描
3.>不在where子句中的'='左边进行函数,算术运算或其他表达式运算,否则系统将无法正确使用索引.
4.>使用索引字段作为条件时,如果该索引是复合索引,那么必须使用到该索引的第一个字段
作为条件时才能保证系统使用该索引,否则该索引将不会被使用.
5.>很多时候可以考虑使用exists代替in
6.>尽量使用数字类型字段
7.>尽可能的使用varchar/nvarchar代替char/nchar
8.>任何地方都不要使用select *from t,用具体的字段列表代替*,不要返回用不到的任何字段
9.>避免频繁创建和删除临时表,以减少系统表资源的消耗
10.>尽量避免使用游标,因为游标的效率很差
11.>在所有的存储过程和触发器的开始设置 set nocount on ,在结束时设置set nocount off
12.>避免大事务操作,提高系统并发能力
13.>避免向客户端返回大数据量,若数据量过大,应该考虑相应需求是否合理

"""
# ----------------------sql注入是如何产生的,如何防止?----------->
"""
产生:
	开发过程中不注意规范书写sql语句和对特殊字符进行过滤,导致客户端可以通过
	全局变量post和get提交一些sql语句正常执行,产生sql注入.
	

防止:
	1.>过滤掉一些常见的数据库操作关键字,或者通过系统函数来进行过滤
	2.>在PHP配置文件中将register_globals=off,设置为关闭状态
	3.>sql语句书写的时候尽量不要省略小引号<tab键上面那个符号>
	4.>提高数据库命名技巧,对于一些重要的字段根据程序的特点命名,取不容易被猜到的
	5.>对于常用的方法加以封装,避免直接暴露sql语句
	6.>开启PHP安全模式,safe_mode=on
	7.>打开magic_quotes_gpc来防止sql注入
	8.>控制错误信息:关闭错误提示信息,将错误信息写到系统日志
	9.>使用mysqli或者pdo预处理

"""
# -------------------NoSQL和关系型数据库的区别?------------------------------->
"""
1.>sql数据库在特定结构的表中,而nosql则更加灵活和可扩展.存储方式可以是json文档,哈希表或者其他方式.
2.>在sql中,必须定义好表和字段结构之后才能添加数据,表结构可以在定义之后更新,但是如果有比较大的结构变更的化就会显得比较复杂.在nosql中,数据可以在任何时候任何地方 添加,不需要先定义表
3.>sql中如果需要增加外部关联数据的话,规范化的做法是在原表中增加一个外键,关联外部数据表,
而在nosql中除了这种方式外,还可以使用非规范化的方式把外部数据直接放到原数据集中,以提高查询效率.缺点是  当更新查询数据的时候会比较麻烦.
4.>sql中可以使用join...on...连接方式将多个关系数据表中的数据用一条简单的查询语句查询出来.nosql暂未提供类似join的查询方式,所以大部分nosql使用非规范化的数据存储方式存储数据
5.>sql中不允许删除已经被使用的外部数据,而nosql中则没有这种强耦合,可以随时删除任何数据.
6.>sql中如果多张表需要同时被更新,即如果一张表更新失败后也不能更新成功.这种场景可以通过事务来控制,可以在所有命令完成后再统一提交事务.而nosql中没有事务这个概念,每一个数据集的操作都是原子性的.
7.>在同水平的系统设计的前提下,因为nosql中省略了join查询的消耗,故理论上性能是优于sql的.
"""
# -------------------------mysql数据库实现分页--------------------------------->
"""
# select * from table limit(第一条数据的起始索引,一页显示多少);
"""
# --------------------------sql语句怎么看效率--------------------------------->
"""
sqlserver2005 --> 新建查询--->输入select * from Person.Contact
执行
"""
# ------------------------优化数据库,提高数据库的性能------------------------->
"""
1.>对语句的优化:
	1.>在程序中,保证实现功能的情况下,尽量减少对数据库的访问次数
	通过搜索参数,尽量减少对表的访问行数,最小化结果集,从而减轻网络负担
	2.>能够分开的操作尽量分开处理,提高每次的响应速度,在数据库窗口使用sql时候,尽量把使用的索引放在选择的首列,算法的结构尽量简单.
	3.>在查询时,不要过多的使用通配符,比如:select * from table1;要用到几列就选择几列,比如:select 字段1,字段2..from table1;
	4.>不要使用数据库游标
	5.>避免不兼容的数据类型,比如float和int,char和varchar是不兼容的
	数据类型的不兼容可能使优化器无法执行一些本来可以进行的优化操作.
	例如:select name from employee where salary > 60000;
	在这条语句中,如salary字段是money类型,则优化器很难对其进行优化,因为60000是个整型数,我们应当在编程时将整型转化为money型,而不要等到运行时候转化.
	如果在查询时候强制转换,查询速度会明显减慢
"""
# --------------------提取数据库中倒数10条数据--------------------->
"""
# select * from table1 order by id desc limit 10;
"""
# ----------------------数据库负载均衡---------------------------->
"""
负载均衡集群是由一组相互独立的计算机系统构成,通过常规网络或专用网络进行连接,由路由器衔接在一起,各节点相互协作,共同负载,均衡压力,对客户端来说,整个群集可以视为一台具有超高性能的独立服务器.

1.>实现原理:实现数据库的负载均衡技术,首先要有一个可以控制连接数据库的控制端,在这里,它截断了数据库和程序直接连接,由所有的程序来访问这个中间层,然后再由中间层来访问数据库.这样,我们就可以具体控制访问某个数据库了,然后还可以根据数据库的当前负载采取有效的均衡策略,来调整每次连接到哪个数据库.

2.>实现多个数据库同步:
	对于负载均衡,最重要的就是所有服务器的数据都是实时同步的.这是一个集群所必需的,因为,如果数据不实时,不同步,那么用户从一台服务器读出来的数据,就和另外一台服务器读取出来的数据不一致了.这是不被允许的.所以必须实现数据库的数据同步.这样,在查询的时候就可以有多个资源,实现均衡,比价常用的方法是moebius for sql server 集群,moebius for sql server 集群,采用将核心程序驻留在每个机器的数据库中的办法,这个核心程序称为moebius for sql server中间件.主要作用是监测数据库内数据的变化并将变化的数据同步到其他数据库中,数据同步完成后客户端才会得到响应,同步过程是并发完成的,所以同步到多个数据库和同步到一个数据库的时间基本相等.另外同步的过程是在事务的环境下完成的 ,保证了多份数据在任何时刻 数据的一致性.正因为moebius中间件宿主在数据库中的创新,让中间件不但能知道数据的变化,而且知道引起数据变化的sql语句.根据sql语句的类型智能的采取不同的数据同步的策略以保证数据同步成本的最小化.
	
	数据条数少,数据内容也不大,则直接同步数据.数据条数很少.但是里面包含大数据类型,比如文本,二进制数据等.则先对数据进行压缩然后再同步,从而减少网络带宽的占用和传输所用的时间.
	
	数据条数少,此时中间件会拿到造成数据变化的sql语句,然后对sql语句进行分析,分析其执行计划和执行成本.并选择是同步数据还是同步sql语句到其他的数据库中.这种情况应用在对表结构进行调整或者批量更改数据的时候,非常有用.

3.>优缺点:

	优点:
	1.>扩展性强:当系统需要更高的数据库处理速度时候,只要简单地增加数据库服务器就可以得到扩展.
	2.>可维护性:当某节点发生故障时,系统会自动检测故障并转移故障节点的应用,保证数据库的持续工作.
	3.>安全性:因为数据库会同步到多态服务器上,可以实现数据集的冗余,通过多份数据来保证安全性,另外它成功地将数据库放到了内网之中,更好地保护了数据库的安全性.
	4.>易用性:对应该用来说完全透明,集群暴露出来的就是一个IP.
	
	缺点:
	
	1.>不能够按照web服务器的处理能力分配负载
	2.>负载均衡器(控制端)故障,会导致整个数据库瘫痪
	
"""
# ---------------------数据库的设计----------------------->
"""
第一范式:数据库表的每个字段都是不可分割的原子数据项,即列不可拆分.
第二范式:在第一范式的基础上,要求数据库表中的每条记录必须是唯一被区分的,即唯一标识.
第三范式:在第二范式的基础上,要求任何非主属性不依赖于其他非主属性,即引用主键
"""
# ----------------------存储过程和函数的区别---------------->
"""
相同点:存储过程和函数都是为了可重复的执行操作数据库的sql语句的集合
1.>存储过程和函数都是一次编译,就会被缓存起来,下次使用就直接选择已经编译好的sql语句,不需要重复使用.减少网络假话,减少网络访问流量.

不同点:
1.>函数中有返回值,且必须有返回值,而过程没有返回值,但是可以通过设置参数类型<in,out>来实现多个参数或者返回值.
2.>存储函数使用select调用,存储过程需要使用call调用
3.>select 语句可以在存储过程中调用,但是除了select...into...之外的语句都不能在函数中使用
4.>通过in out 参数,过程相关函数更加灵活,可以返回多个结果
"""
# -------------------------mysql日志----------------------------------->
"""
错误日志:记录启动,运行或者停止mysql时出现的问题
通用日志:记录建立的客户端连接和执行的语句
二进制日志:记录所有更改数据的语句
慢查询日志:记录所有执行时间超过long_query_time秒的查询或者不适用索引的查询

通过使用--slow_query_log[={0|1}]选项来启用慢查询日志,所有执行时间超过long_query_time的语句都会被记录.
"""














































































