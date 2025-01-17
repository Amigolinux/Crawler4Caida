# coding:utf-8
"""
create on May 1, 22020 by Wayne Yu
Function: 对全球BGP数据进行分析，并针对某一个AS的历史BGP互联信息进行分析

1）CDN企业
Akamai, 32787

2)云服务商
google, 15169
阿里云，45102
腾讯云，132203

03)ISP
AT&T Services,Inc, 7018
Verizon，701
NTT, 2914
电信，4134
联通，4837


Edition:

为地图基础课题第一篇论文输出，重新绘图，使得排版更加的美观
绘制的时间修改为19980101-20191201

"""

import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import time
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def analysis(open_file, as_analysis):
    """
    对数据进行分析处理
    :param open_file:
    :param as_analysis:
    :return:
    """
    file_read = open(open_file, 'r', encoding='utf-8')
    edge_cnt = 0
    peer_cnt = 0
    transit_provider_cnt = 0
    transit_customer_cnt = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip().split('|'))
        if line.strip().split('|')[0] == as_analysis:  # 如果位于第一位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_provider_cnt += 1
            edge_cnt += 1

        if line.strip().split('|')[1] == as_analysis:  # 如果位于第二位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_customer_cnt += 1
            edge_cnt += 1
        # if edge_cnt > 1000:
        #     break

    return edge_cnt, peer_cnt, transit_provider_cnt + transit_customer_cnt,transit_provider_cnt, transit_customer_cnt


def draw(draw_date, data_list, as_analysis):
    """
    对传入的数据进行绘图
    :param draw_date:
    :param data_list:
    :return:
    """
    print(data_list)
    # 存储绘图数据
    save_path_data_list = "../000LocalData/Paper_Data/draw_AS" + as_analysis+".csv"
    write_to_csv(data_list, save_path_data_list)

    dt = 1
    # t = np.arange(0, len(draw_date), dt)
    edge_list = []
    peer_list = []
    transit_list = []
    transit_provider_list = []
    transit_customer_list = []
    for item in data_list:
        print(int(item[0]))
        edge_list.append(int(item[0]))
        peer_list.append(int(item[1]))
        transit_list.append(int(item[2]))
        transit_provider_list.append(int(item[3]))
        transit_customer_list.append(int(item[4]))

    fig, ax = plt.subplots(1, 1, figsize=(19.2, 10.8))
    plt.xticks(rotation=32)
    plt.tick_params(labelsize=32)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    font = {'family': 'Times New Roman',
            'style': 'normal',
            'weight': 'normal',
            'color': 'black',
            'size': 42
            }
    font_legend = {'family': 'Times New Roman',
                   'style': 'normal',
                   'weight': 'normal',
                   'size': 32
                   }
    tick_spacing = 12
    # title_string = "全球互联网BGP互联趋势分析(19980101-20191201) AS:" + as_analysis
    # ax.set_title(title_string, font)
    ax.plot(draw_date, edge_list, ls='-', marker='.', label='Total interconnections')
    ax.plot(draw_date, peer_list, ls=':', marker='+', label='Peer')
    ax.plot(draw_date, transit_list, ls='-.', marker='s', label='Transit')
    ax.plot(draw_date, transit_provider_list, ls=':', marker='v', label='Transit-ISP')
    ax.plot(draw_date, transit_customer_list, ls=':', marker='^', label='Transit-Customer')
    ax.set_xlabel('Time of estimation', font)
    ax.set_ylabel('Interconnection', font)
    ax.legend(prop=font_legend)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.grid(True)
    fig.tight_layout()
    save_path_fig = "../000LocalData/Paper_Data/draw_AS" + as_analysis+"_en.svg"
    plt.savefig(save_path_fig, dpi=600)
    save_path_fig = "../000LocalData/Paper_Data/draw_AS" + as_analysis+"_en.pdf"
    plt.savefig(save_path_fig, dpi=600)
    # plt.show()


if __name__ == "__main__":
    # as_analysis = ["32787", "13335", "54994", "63541",
    #                "16509", "8075", "15169", "37963", "45102", "45090", "132203", "38365", "55967",
    #                "4134", "4837", "7018", "701", "2914"]
    as_analysis = ["7018", "2914", "32787", "15169", "45102", "4134", "4837"]
    # file_path = ["../000LocalData/as_relationships/20151201.as-rel2.txt",
    #              "../000LocalData/as_relationships/20160901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20170901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20180901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20190901.as-rel2.txt"]
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-4"):
        for file_item in files:
            # print(os.path.join(root, file_item))
            file_path.append(os.path.join(root, file_item))
    print(file_path)
    result_list = []
    date_list = []
    for as_item in as_analysis:
        for path_item in file_path:
            result_list.append(analysis(path_item, as_item))
            print(result_list)
            temp_str = path_item.split('\\')[-1]
            date_list.append(temp_str.split('.')[0])
        draw(date_list, result_list, as_item)
        result_list = []  # 清空result_list
        date_list = []  # 清空date_list
