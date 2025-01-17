# 工具文件:  负责实现具体的功能(函数)
card_list = []  # 名片列表 包含学生信息(字典)  全局变量


def show_menu():
    """显示界面"""
    print("*" * 30)
    print("欢迎使用[名片管理系统] V1.0")
    print()
    print("1.新建名片")
    print("2.显示全部")
    print("3.查询名片")
    print()
    print("0.退出系统")
    print("*" * 30)


def add_card():
    """新建名片"""
    print("功能: 新建名片")
    # 获取用户输入
    name_str = input("请输入姓名:")
    phone_num = input("请输入电话:")
    qq_num = input("请输入qq号码:")
    mail_adr = input("请输入邮箱:")
    # 将信息封装到字典中 方便使用
    card_info = {"name": name_str, "phone": phone_num, "qq": qq_num, "mail": mail_adr}
    # 将字典添加到全局列表中保存 方便其他函数使用
    card_list.append(card_info)
    print("添加%s的名片成功" % name_str)


def show_all():
    """显示全部"""
    print("功能: 显示全部")
    # 判断是否有名片信息
    if len(card_list) == 0:
        print("提示:没有任何名片记录")
        return
    print("姓名\t\t电话\t\tqq\t\t邮箱")
    print("-" * 30)
    # 取出全局列表中的每一个学生信息(字典)
    for card_info in card_list:
        # 格式化操作
        print("%s\t\t%s\t\t%s\t\t%s" % (
            card_info["name"], card_info["phone"], card_info["qq"], card_info["mail"]))
    print("-" * 30)
