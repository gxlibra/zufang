#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# __Author__ = 'gao'

from bs4 import BeautifulSoup
import requests
import csv


def Request58(address, money):
    """
    address: 地址
    money: 租金
    """
    url = 'http://{address}.58.com/pinpaigongyu/pn/{page}/?minprice={money}'

    # 已完成的页数序号,初始为0
    page = 0

    csv_file = open('58_{}.csv'.format(address), 'a', encoding='utf-8')
    csv_writer = csv.writer(csv_file, delimiter=',')

    while True:
        page += 1
        print('fetch:', url.format(address=address, page=page, money=money))
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/69.0.3497.92 Safari/537.36'
        }
        response = requests.get(url.format(address=address, page=page, money=money), headers=headers)
        html = BeautifulSoup(response.text)
        house_list = html.select('.list > li')

        # 循环在读不到新的房源时结束
        if not house_list:
            break

        for house in house_list:
            house_title = house.select('h2')[0].string
            house_url = 'http://bj.58.com/%s' % (house.select('a')[0]['href'])
            house_info_list = house_title.split()

            # 如果第二列是公寓名则取第一列为地址
            if '公寓' in house_info_list[1] or '青年社区' in house_info_list[1]:
                house_location = house_info_list[0]
            else:
                house_location = house_info_list[0]

            house_money = house.select('.money')[0].select('b')[0].string
            csv_writer.writerow([house_title, house_location, house_money, house_url])

    csv_file.close()


if __name__ == '__main__':
    money = {
        # 租金价格
        '1': '600_1000',
        '2': '1000_1500',
        '3': '1500_2000',
        '4': '2000_3000',
        '5': '3000_5000',
        '6': '5000_8000',
        '7': '8000_20000',
    }
    # print(money.get('1'))
    Request58('bj', money.get('4'))

