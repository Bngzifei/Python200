"""

3D 图形需要的数据与等高线图基本相同：X、Y 数据决定坐标点，Z 轴数据决定 X、Y 坐标点对应的高度。与等高线图使用等高线来代表高度不同，3D 图形将会以更直观的形式来表示高度。

为了绘制 3D 图形，需要调用 Axes3D 对象的 plot_surface() 方法来完成。

下面程序将使用与前面等高线图相同的数据来绘制 3D 图形，此时将看到程序会以更直观的形式来显示高度。

"""


import matplotlib.pyplot as plt

import numpy as np
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure(figsize=(12, 8))
ax = Axes3D(fig)


delta = 0.125


# 生成代表X轴数据的列表
x = np.arange(-3.0, 3.0, delta)

# 生成代表Y轴数据的列表
y = np.arange(-2.0, 2.0, delta)


# 对x,y数据执行网格化
X, Y = np.meshgrid(x, y)


Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)


# 计算Z轴数据(高度数据)
Z = (Z1 - Z2) * 2


# 绘制3D图形
ax.plot_surface(X, Y, Z,
                rstride=1,  # rstride(row)指定行的跨度
                cstride=1,  # cstride(column)指定列的跨度
                cmap=plt.get_cmap("rainbow")  # 设置颜色映射
                )


# 设置Z轴范围
ax.set_zlim(-2, 2)


# 设置标题
plt.title("3D图")
plt.show()
