import csv
import os


# 获取所有文件
def getAllDataPath():
    path = './data'
    files = os.listdir(path)
    return files


# 获取文件中项目号
def getAllProjectId(file):
    path = './data/'
    csvFile = open(path + file, 'r', encoding="GB18030")
    reader = csv.reader(csvFile)
    idList = []
    for item in reader:
        if item[5] == '项目编号':
            continue
        idList.append(item[5])
    return idList


# 替换url字符串内的信息，方便访问
def changeUrl(url):
    str_head = '/kns8/Detail'
    url = url.replace(str_head, '/kcms/detail/detail.aspx')
    result = 'https://www.cnki.net' + url
    return result


# 存储json文件
def saveJson(fundId, jsonList):
    path = './crawlerData'
    for i in range(len(jsonList)):
        file_name = path + f'/{fundId}_{i}.json'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(jsonList[i])

# 替换作者链接，方便访问
# /kns8/Detail?sdb=CJFD&sfield=%e4%bd%9c%e8%80%85&skey=%e5%91%a8%e4%b9%89%e6%a3%8b&scode=000014666066&acode=000014666066
# 转换为
# https://kns.cnki.net/kcms/detail/knetsearch.aspx?dbcode=CJFD&code=000014666066&sfield=au&skey=%e5%91%a8%e4%b9%89%e6%a3%8b&uniplatform=NZKPT
def changeAuthor(url):
    url = url[13:]
    url_split = url.split('&')
    sdb = url_split[0][4:]
    sfield = url_split[1][7:]
    skey = url_split[2][5:]
    scode = url_split[3][6:]
    acode = url_split[4][6:]
    result = f'https://kns.cnki.net/kcms/detail/knetsearch.aspx?dbcode={sdb}&code={scode}&sfield=au&skey={skey}&uniplatform=NZKPT'
    return result
