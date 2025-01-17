import pygame  # 动态模块.dll.pyd 静态模块:.py 静态的必须导入模块名.
import sys
from pygame.locals import *
import time
import random

"""
1.创建窗口
2.加载背景图片
3.把背景图片贴到窗口
4.刷新窗口

子弹的y = 英雄飞机的y - 子弹的高度
子弹的x = 英雄飞机的x + 英雄飞机宽的一半 - 子弹宽的一半
"""


class Item:
	"""界面元素类"""
	window = None  # 类属性

	def __init__(self, img_path, x, y):
		self.img = pygame.image.load(img_path)  # 图片
		self.x = x  # 记录图片位置
		self.y = y

	def display(self):
		"""显示飞机"""
		self.window.blit(self.img, (self.x, self.y))


class Map(Item):
	"""地图类"""
	pass


class Bullet(Item):
	"""子弹类"""

	def move(self):
		"""子弹移动"""
		print('bullet move up')
		self.y -= 10

	def __del__(self):
		"""验证子弹是否销毁"""
		print('子弹销毁了')


class BasePlane(Item):
	"""飞机基类"""
	pass


class EnemyPlane(BasePlane):
	"""敌机类"""

	def move_down(self):
		"""敌机下移"""
		print('downing')
		self.y += 5
		if self.y >= 768:
			self.y = random.randint(-300, -68)
			self.x = random.randint(0, 412)
			self.img = pygame.image.load('res/img-plane_%d.png' % random.randint(1, 7))


class HeroPlane(BasePlane):
	"""英雄飞机类"""

	def __init__(self, img_path, x, y):
		super().__init__(img_path, x, y)
		self.bullets = []  # 保存所有子弹

	def move_left(self):
		"""飞机左移"""
		print('left')
		self.x -= 5

	def move_right(self):
		"""飞机右移"""
		print('right')
		self.x += 5

	def fire(self):
		"""开火"""
		# 1.创建子弹对象
		bullet = Bullet('res/bullet_14.png', self.x + 50, self.y - 56)
		self.bullets.append(bullet)  # 添加到子弹列表

	def display_bullet(self):
		"""处理子弹的显示问题"""
		temp_list = []  # 记录要销毁的子弹
		for bullet in self.bullets:
			if bullet.y > -56:  # 没有飞出去,继续贴图
				bullet.display()  # 重复贴子弹图
				bullet.move()
			else:
				# self.bullets.remove(bullet)  # 飞出去销毁子弹
				temp_list.append(bullet)  # 把超出窗口的子弹添加到临时列表

		for del_bullet in temp_list:  # 销毁子弹
			self.bullets.remove(del_bullet)


def main():
	# 1.创建窗口
	window = pygame.display.set_mode((512, 768))
	Item.window = window  # 给类属性赋值 只能是使用类对象进行赋值,实例对象虽然可以访问类属性,但是不能进行赋值操作.

	# 2.加载背景图片
	map1 = Map('res/img_bg_level_1.jpg', 0, 0)

	# 2.1 创建英雄飞机实例对象
	hero_plane = HeroPlane('res/hero2.png', 196, 600)

	# 创建敌机实例对象
	enemy_plane_list = []
	for i in range(8):
		enemy_plane = EnemyPlane('res/img-plane_%d.png' % random.randint(1, 5), random.randint(0, 412),
								 random.randint(-300, -68))  # 将敌机的位置设置成随机的x,y.
		enemy_plane_list.append(enemy_plane)

	while True:
		# 3.0把背景图片贴到窗口上
		map1.display()
		# 3.1把飞机图贴到窗口上 重复贴
		hero_plane.display()
		# 3.2 遍历子弹列表,取出每一个子弹,让每一个子弹都重复贴图
		hero_plane.display_bullet()

		# 3.3 贴敌机图
		for enemy_plane in enemy_plane_list:
			enemy_plane.display()
			enemy_plane.move_down()

		# 4.刷新窗口,不刷没法显示以上效果
		pygame.display.update()

		# 获取新事件
		for event in pygame.event.get():
			# 1. 鼠标点击关闭窗口事件
			if event.type == QUIT:  # 判断是不是退出
				print("点击关闭窗口按钮")
				sys.exit()  # 关闭程序

			# 2. 键盘按下事件  # 只是一个单按事件,单击事件
			if event.type == KEYDOWN:
				# 判断用户按键
				if event.key == K_SPACE:
					print("space")
					hero_plane.fire()  # 这里只会贴一次

		# 键盘长按事件
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
			hero_plane.fire()
			hero_plane.move_left()
		if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
			hero_plane.fire()
			hero_plane.move_right()

		time.sleep(0.02)  # 执行到这里的时候,程序会暂停0.02秒,为了让cpu缓一缓 提高效率cpu.


if __name__ == '__main__':
	main()
