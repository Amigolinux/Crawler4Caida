# coding:utf-8
"""
create on May 29, 2020 By Wenyan YU
Function：

缘起新型互联网交换中心，感谢PeeringDB给了面试数据分析的基础，时间过去已近三年
今天再回过头来看PeeringDB，不禁感慨万千
我经常跟自己说，未来是数据的时代，数据资源的积累，数据处理方法论的探索，大数据技术的研究便显得非常重要

该程序的主要目的是再次探索分析PeeringDB的IX信息（https://www.peeringdb.com/api/ix）
{'id': 1,
'org_id': 2,
'name': 'Equinix Ashburn',
'name_long': 'Equinix Ashburn Exchange',
'city': 'Ashburn',
'country': 'US',
'region_continent': 'North America',
'media': 'Ethernet',
'notes': '',
'proto_unicast': True,
'proto_multicast': False,
'proto_ipv6': True,
'website': 'https://ix.equinix.com',
'url_stats': '',
'tech_email': 'support@equinix.com',
'tech_phone': '',
'policy_email': 'support@equinix.com',
'policy_phone': '',
'net_count': 324,
'created': '2010-07-29T00:00:00Z',
'updated': '2016-11-23T21:40:34Z',
'status': 'ok'}

可借助IX创建的时间以及国家、城市、大洲的信息进行相关分析，包括是否支持IPV6等

1）当前时间全球IXP总数的统计
2）全球IXP发展趋势
3）全球IXP信息按国家（地区）维度统计
4）全球IXP信息按大洲维度统计
5）我国IXP发展具体情况
6）全球IXP的IPV6支持情况
7）案例1：阿姆斯特丹交换中心（AMS-IX）数据统计分析(https://peeringdb.com/api/ix/26)
8）案例2：香港交换中心（HK-IX）数据统计分析
9）案例3：莫斯科交换中心（MSK-IX Moscow）数据统计分析

以上所有数据均可实时统计，可基于PeeringDB的数据一键生产当前时间【全球互联网交换中心的数据分析报告（PEERING DB）】

ix的详细信息：
{"id": 26,
"org_id": 2634,
"org": {"id": 2634,
        "name": "Amsterdam Internet Exchange BV",
        "aka": "",
        "name_long": "",
        "website": "http://www.ams-ix.net/",
        "notes": "",
        "net_set": [3363, 4277, 6471, 14259, 14260],
        "fac_set": [],
        "ix_set": [26, 366, 577, 935, 944, 1623],
        "address1": "Frederiksplein 42",
        "address2": "",
        "city": "Amsterdam",
        "country": "NL",
        "state": "Noord Holland",
        "zipcode": "1017XN",
        "floor": "",
        "suite": "",
        "latitude": null,
        "longitude": null,
        "created": "2010-08-11T15:40:42Z",
        "updated": "2020-02-19T04:08:04Z",
        "status": "ok"},
"name": "AMS-IX",
"aka": "",
"name_long": "Amsterdam Internet Exchange",
"city": "Amsterdam",
"country": "NL",
"region_continent": "Europe",
"media": "Ethernet",
"notes": "",
"proto_unicast": true,
"proto_multicast": false,
"proto_ipv6": true,
"website": "http://www.ams-ix.net/",
"url_stats": "https://www.ams-ix.net/statistics/",
"tech_email": "noc@ams-ix.net",
"tech_phone": "+31205141717",
"policy_email": "info@ams-ix.net",
"policy_phone": "+31203058999",
"fac_set": [...],
"ixlan_set": [...],
"net_count": 820,
"fac_count": 25,
"ixf_net_count": 0,
"ixf_last_import": null,
"service_level": "Not Disclosed",
"terms": "Not Disclosed",
"created": "2010-07-29T00:00:00Z",
"updated": "2020-01-22T04:24:06Z",
"status": "ok"}]


"""
from urllib.request import urlopen
import json
from datetime import *
import time


def generate_global_ixp_report():
    """
    基于PEERING DB数据一键生成当前时间【全球互联网交换中心数据分析报告（PEERING DB）】
    :return:
    """
    html = urlopen(r'https://www.peeringdb.com/api/ix')
    html_json = json.loads(html.read())
    # print(html_json)
    ixp_cnt_year = {}  # 统计每年IXP的数量
    country_dict = {}  # 统计当前时间每个国家的IXP数量
    region_dict = {}  # 统计当前时间每个大洲的IXP数量

    ixp_cn = []  # 中国大陆的IXP
    ixp_hk = []  # 香港地区
    ixp_tw = []  # 台湾地区

    ipv6_on_cnt = 0  # 统计支撑ipv6的交换中心
    ipv6_off_cnt = 0  # 统计不支持ipv6的交换中心

    for item in html_json['data']:
        # 利用datetime处理时间字符串
        dt_create = datetime.strptime(item['created'], '%Y-%m-%dT%H:%M:%SZ')
        # print(dt_create)
        # 创建时间统计
        if dt_create.year not in ixp_cnt_year.keys():
            ixp_cnt_year[int(dt_create.year)] = 1
        else:
            ixp_cnt_year[int(dt_create.year)] = ixp_cnt_year[int(dt_create.year)] + 1
        # 按国家统计
        if item['country'] not in country_dict.keys():
            country_dict[item['country']] = 1
        else:
            country_dict[item['country']] = country_dict[item['country']] + 1
        # 按大洲统计
        if item['region_continent'] not in region_dict.keys():
            region_dict[item['region_continent']] = 1
        else:
            region_dict[item['region_continent']] = region_dict[item['region_continent']] + 1
        # 统计我国IXP相关情况
        temp = []
        if item['country'] == 'CN':
            temp.append(item['name'])
            temp.append(item['created'])
            temp.append(item['website'])
            temp.append(item['name_long'])
            ixp_cn.append(temp)

        temp = []
        if item['country'] == 'HK':
            temp.append(item['name'])
            temp.append(item['created'])
            temp.append(item['website'])
            temp.append(item['name_long'])
            ixp_hk.append(temp)

        temp = []
        if item['country'] == 'TW':
            temp.append(item['name'])
            temp.append(item['created'])
            temp.append(item['website'])
            temp.append(item['name_long'])
            ixp_tw.append(temp)
        # print(item['proto_ipv6'])
        if item['proto_ipv6']:
            ipv6_on_cnt += 1
        else:
            ipv6_off_cnt += 1

    print("- - - - - - -0)全球互联网交换中心数据分析报告（PEERING DB）- ")
    print("报告生成时间：", datetime.now())
    print("基础数据来源：https://www.peeringdb.com/")
    print("- - - - - - -1)当前时间全球IXP总数统计- - - - - - - - - - - -")
    print("Global IXP Count:", len(html_json['data']))
    print("- - - - - - -2)全球IXP发展趋势- - - - - - - - - - - -")
    ixp_cnt_year_list = []  # 存储统计列表
    for key in ixp_cnt_year.keys():
        ixp_cnt_year_list.append([key, ixp_cnt_year[key]])
    ixp_cnt_year_list.sort(key=lambda elem: int(elem[0]))
    # print(ixp_cnt_year_list)
    print("全球互联网自2010年至今，每年新增的IXP数量:")
    for item in ixp_cnt_year_list:
        print(item[0], "年新增IXP数量(个):", item[1])
    print("全球互联网自2010年至今，每年总计的IXP数量:")
    total_ixp = 0
    for item in ixp_cnt_year_list:
        total_ixp += int(item[1])
        print(item[0], "年总计IXP数量(个):", total_ixp)
    print("- - - - - - -3)全球IXP信息按国家（地区）维度统计- - - - - - - - - - - -")
    country_dict_list = []  # 存储统计列表
    for key in country_dict.keys():
        country_dict_list.append([key, country_dict[key]])
    country_dict_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    # print(country_dict_list)
    print("全球范围内共有", len(country_dict_list), "个国家（地区）部署了IXP")
    print("按IXP数量降序排名，TOP 20信息如下：")
    for item in country_dict_list[0:20]:
        print(item[0], ":", item[1])
    print("- - - - - - -4)全球IXP信息按大洲维度统计- - - - - - - - - - - -")
    region_dict_list = []  # 存储统计列表
    for key in region_dict.keys():
        region_dict_list.append([key, region_dict[key]])
    region_dict_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    print("按照IXP数量降序排名，各大洲IXP数量分布如下：")
    for item in region_dict_list:
        print(item[0], ":", item[1])
    print("- - - - - - -5)我国IXP发展具体情况- - - - - - - - - - - -")
    print("我国大陆地区CN的IXP数量:", len(ixp_cn), "，其详细信息如下：")
    for item in ixp_cn:
        print(item[0], ",", item[1], ",", item[2], ",", item[3])
    print("我国香港地区HK的IXP数量:", len(ixp_hk), "其详细信息如下：")
    for item in ixp_hk:
        print(item[0], ",", item[1], ",", item[2], ",", item[3])
    print("我国台湾地区TW的IXP数量:", len(ixp_tw), "其详细信息如下：")
    for item in ixp_tw:
        print(item[0], ",", item[1], ",", item[2], ",", item[3])
    print("- - - - - - -6)全球IXP的IPV6支持情况- - - - - - - - - - - -")
    print("已支持IPV6的IXP数量：", ipv6_on_cnt)
    print("未支持IPV6的IXP数量：", ipv6_off_cnt)
    print("- - - - - - -7)案例1：阿姆斯特丹交换中心（AMS-IX）数据统计分析- - - - - -")
    html = urlopen(r'https://peeringdb.com/api/ix/26')
    html_json = json.loads(html.read())
    # print(html_json['data'][0])
    ix_data = html_json['data'][0]
    print("IXP名称(简称):", ix_data['name'])
    print("IXP名称(全称):", ix_data['name_long'])
    print("IXP所在城市及国家:", ix_data['city'], ", ", ix_data['country'], ", ", ix_data['region_continent'])
    print("是否支持IPV6:", ix_data['proto_ipv6'])
    print("官方网站:", ix_data['website'])
    print("该IXP流量信息展示页面:", ix_data['url_stats'])
    print("该IXP接入网络数量:", ix_data['net_count'])
    print("该IXP网络基础设施点:")
    item_cnt = 1
    for item in ix_data['fac_set']:
        print(item_cnt, "> ", item['name'], ", ", item['city'], ", ", item['country'])
        item_cnt += 1
    print("- - - - - - -8)案例2：香港交换中心（HK-IX）数据统计分析- - - - - -")
    html = urlopen(r'https://peeringdb.com/api/ix/42')
    html_json = json.loads(html.read())
    # print(html_json['data'][0])
    ix_data = html_json['data'][0]
    print("IXP名称(简称):", ix_data['name'])
    print("IXP名称(全称):", ix_data['name_long'])
    print("IXP所在城市及国家:", ix_data['city'], ", ", ix_data['country'], ", ", ix_data['region_continent'])
    print("是否支持IPV6:", ix_data['proto_ipv6'])
    print("官方网站:", ix_data['website'])
    print("该IXP流量信息展示页面:", ix_data['url_stats'])
    print("该IXP接入网络数量:", ix_data['net_count'])
    print("该IXP网络基础设施点:")
    item_cnt = 1
    for item in ix_data['fac_set']:
        print(item_cnt, "> ", item['name'], ", ", item['city'], ", ", item['country'])
        item_cnt += 1
    print("- - - - - - -9)案例3：莫斯科交换中心（MSK-IX Moscow）数据统计分析- - - - - -")
    html = urlopen(r'https://peeringdb.com/api/ix/100')
    html_json = json.loads(html.read())
    # print(html_json['data'][0])
    ix_data = html_json['data'][0]
    print("IXP名称(简称):", ix_data['name'])
    print("IXP名称(全称):", ix_data['name_long'])
    print("IXP所在城市及国家:", ix_data['city'], ", ", ix_data['country'], ", ", ix_data['region_continent'])
    print("是否支持IPV6:", ix_data['proto_ipv6'])
    print("官方网站:", ix_data['website'])
    print("该IXP流量信息展示页面:", ix_data['url_stats'])
    print("该IXP接入网络数量:", ix_data['net_count'])
    print("该IXP网络基础设施点:")
    item_cnt = 1
    for item in ix_data['fac_set']:
        print(item_cnt, "> ", item['name'], ", ", item['city'], ", ", item['country'])
        item_cnt += 1


if __name__ == "__main__":
    time_start = time.time()
    generate_global_ixp_report()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
