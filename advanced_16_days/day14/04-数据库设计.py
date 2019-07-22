print('------------------')
"""
带有实际场景的去思考,去学习.

如果有外键的情况下:
先创建主表,再去创建子表

设计表结构:观摩别人的表结构:
三范式:遵守到2范式或者3范式即可

只支持二维表

第一范式<1NF>:原子性,即列不能够再分成其他几列--->不存在嵌套的表结构

第二范式<2NF>:必须是1NF,1.>另外还需要包含一个主键,2.>非主键字段必须完全依赖于主键,不能只依赖于主键的一部分.

有时候会将2个字段设置为主键,这时候其他非主键字段如果是依赖于主键中的某一个字段,那么就不是第二范式了.
示例:
产品ID 订单ID 产品名称 价格  产品名称和价格只依赖于主键中的产品ID,和订单ID无关.这样就是部分依赖

第三范式:前提必须是第二范式
不允许存在 非主键字段和主键字段 的 传递依赖关系
传递依赖 A-->B -->C 这样A对C就有一个间接依赖

办法:拆分表结构-->直到没有可被细分的表,这样就去除了AC之间的间接依赖

非主键A-->B-->C主键


订单ID 订单时间  用户ID  用户地址


E-R模型:实体联系图 
矩形:实体/表名
椭圆:字段名/列表/属性名
菱形:多对对的关系,也是一个表名,必须转换成一对多的关系
线条:关系/也是一种数据

多对多的关系:
A B之前如果多对多,那么就找一个中间表C来进行中转
https://mp.weixin.qq.com/s/Yjh_fPgriuhhOZyVtRQ-SA?

"""