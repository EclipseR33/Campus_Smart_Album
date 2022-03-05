import requests
from lxml import etree
import csv


def get_new_pneumonia():
    appid = "97271352"
    appsecret = "aCVHN6c7"
    version = "epidemic"
    url = 'https://tianqiapi.com/api?version=' + version + '&appid=' + appid + '&appsecret=' + appsecret
    res = requests.post(url).json()
    print(res)
    errcode = res["errcode"]
    try:
        data = res["data"]
        f = open('data.txt', 'w')
        f.write(str(res))
    except Exception as e:
        print(e)


def get_confirmed_data():
    path = 'data/time_series_covid_19_confirmed.csv'
    data = []
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for i, rows in enumerate(reader):
            # 日期改动
            if i == 0:
                temp = []
                for row in rows:
                    if row[:2] == '20':
                        row = row[3:]
                    temp.append(row)
                rows = temp
                data.append(rows[4:])
            else:
                data.append(rows[4:])
    print(data)


if __name__ == "__main__":
    get_confirmed_data()
