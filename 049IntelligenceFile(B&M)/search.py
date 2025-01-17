# coding:utf-8
"""
create on Aug 20, 2020 by Wenyan YU
Email: ieeflsyu@outlook.com

Function:

该程序主要是为了搜索出给定路径中全部文件

"""

import os
import time


KEY_WORDS = ["内部"]  # 存储需要检索的关键词


def search_file(root_dir):
    """
    根据传入的根目录信息，检索该目录下所有文件
    :param root_dir:
    :return:
    """
    print("需检索路径：", root_dir)
    file_path_list = []  # 存储当前文件夹内所有路径
    file_dict = dict()  # 存储所有的文件类型
    for root, dirs, files in os.walk(root_dir):
        for file_item in files:
            file_path = os.path.join(root, file_item)
            file_type = os.path.splitext(file_item)[-1]
            # print(file_path)
            # print(file_type)

            if file_type == ".txt":
                print(file_path)
                file_analysis_txt(file_path)

            if file_type in file_dict.keys():
                file_dict[file_type].append(file_path)
            if file_type not in file_dict.keys():
                file_dict[file_type] = [file_path]

            file_path_list.append(file_path)
    print("该路径中检索到的所有文件记录：", len(file_path_list))
    for key in file_dict.keys():
        if len(key) < 10:
            print("该路径中%s文件类型的数量为%s个" % (key, len(file_dict[key])))


def file_analysis_txt(aim_file):
    """
    根据传入的txt file，对其做字符串检索
    :param aim_file:
    :return:
    """
    try:
        file_read = open(aim_file, 'r', encoding='gbk')

        temp_line_list = []  # 存储检索到的行信息

        for line in file_read.readlines():
            for keyword in KEY_WORDS:
                if line.find(keyword) != -1:
                    # print(line)
                    temp_line_list.append(line)

        if len(temp_line_list) != 0:
            print(aim_file)
            print(temp_line_list)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动的时间
    input_dir = "C:/"
    search_file(input_dir)
    time_end = time.time()  # 记录程序结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "s")