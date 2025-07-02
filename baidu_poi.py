#!usr/bin/env python

"""
@Author: SMnRa
@Email: smnra@163.com
@Project: baidu_polygon
@File: baidu.py
@Time: 2019/05/09 9:53

功能描述: 百度地图 电子边框


"""
import time,json,os,random
from fake_useragent import UserAgent
import coordinateTranslate

from initPlaywright import init_playwright







# 初始化坐标系转化对象
coordTrans = coordinateTranslate.GPS()
def miToGPS(lon, lat):
    coord = coordTrans.convert_BD09MI_to_WGS84(float(lon), float(lat))
    return coord


def getUserAgent():
    ua = UserAgent()  # 初始化 随机'User-Agent' 方法
    tmpuserAnent =  'user-agent="'+ ua.random + '"'
    return tmpuserAnent


def isJsonStr(jsonStr):
    # 判断一个字符串似否是json格式
    try:
        json.loads(jsonStr)
    except ValueError:
        return False
    return True



def toJson(text):
    # 字符串 反序列化
    try:
        if isJsonStr(text):
            return json.loads(text)
    except Exception as e:
        print(e)
        return ''


def isDictKey(mDict, *mKey):
    # 判断 字典 mDict 存在 mKey, 并且 mKey 的值为 字典类型 返回True 否则返回 False
    tempDict = dict(mDict)
    tag = True  # 是否无效标记
    rdict = None
    for key in mKey:
        if key in tempDict.keys() and isinstance(tempDict[key], dict):
            tempDict = tempDict.get(key, '')
            if not isinstance(tempDict, dict):
                print(key, "is not dict.")
                tag = False
            else:
                tag = True
        else:
            tag = False
    if tag:
        rdict = dict(tempDict)
    return rdict


def clearCoord(coordStr):
    # 整理坐标数据
    coordStr = coordStr.split('|')[2]
    coordStr = coordStr.replace("1-", "").replace(";", "")
    coordList = '[' + coordStr + ']'
    coordList = eval(coordList)
    return list(zip(*(iter(coordList),) * 2))


def stripStr(tmp):
    # 删除字符串中的不可见字符
    result = str(tmp)
    result = result.strip()
    result = result.replace(",", ';')
    result = result.replace("\n", '')
    result = result.replace("\r", '')
    result = result.replace("\t", ' ')
    result = result.strip()
    return result


def init_csv_title(csvName=r'./baidu.csv' ):
    # 如果不存在r'./baidu.csv'  则建立并写入表头
    if not os.path.isfile(csvName):
        with open(csvName, mode='a+', encoding='gbk', errors=None) as f:  # 将表头写入文件
            f.writelines("csvName,name,uid,primary_uid,alias,addr,address_norm,area,area_name,catalogID,di_tag,std_tag,std_tag_id,tel,x,y,lon,lat,geo\n")


def baidu_map_init():
    # 获取实例
    playwright, browser, page = init_playwright(isPersistent=True, isHeadless=False)  # 有痕模式
    # playwright, browser,page = init_playwright(isPersistent=False, isHeadless=False)   # 无痕模式
    try:
        page.goto("https://map.baidu.com/")
        page.wait_for_load_state(state="networkidle")
        page.wait_for_load_state(state="domcontentloaded")

        # 暂停2秒，已达到完全模拟浏览器的效果
        time.sleep(random.randint(1, 10)*0.3)

        # 等待 搜索框元素 加载完成
        page.wait_for_selector('xpath=//input[@id="sole-input"]')
        search_input = page.query_selector('xpath=//input[@id="sole-input"]')


        return playwright, browser, page
    except Exception as e:
        print(e)







def get_poi_info(browser,buildName):
    searchUrl = 'http://api.map.baidu.com/?qt=s&c=131&rn=100&ie=utf-8&oue=1&res=api&wd='
    url = searchUrl + buildName

    # 在新标签中打开url
    resultPage = browser.new_page()
    resultPage.goto(url)
    resultTag = resultPage.query_selector('xpath=/html/body/pre')
    resultText = resultTag.inner_text()
    resultJson = toJson(resultText)
    resultPage.close()
    return resultJson


def searchPoi(browser, buildName):
    # 在百度地图搜索框中搜索 buildName 保存到csv文件中

    # 获取搜索栏poi数据
    resultJson = get_poi_info(browser, buildName)

    poiInfo = []
    if isinstance(resultJson, dict):
        # result 字典存在 key  'content' 并且 result['content'] 是列表
        if 'content' in resultJson.keys() and isinstance(resultJson['content'], list):
            pois = resultJson.get('content')  # poi的列表
        else:
            print(" Not found poi.")
            return False

        for poi in pois:
            (pylgon, geoMi, x, y, lon, lat) = [[], '', '', '', '', '']  # 清空变量
            try:
                geoMi = isDictKey(poi, 'ext', 'detail_info', 'guoke_geo')
                if isinstance(geoMi, dict):
                    geoMi = geoMi.get('geo', '')
                    if geoMi:
                        # 如果存在 多边形边界
                        poiGeo = clearCoord(geoMi)
                        # print(poiGeo)
                        for coord in poiGeo:
                            # 由百度墨卡托坐标系 转换为 WGS-84 坐标系
                            gps = miToGPS(coord[0], coord[1])
                            pylgon.append([str(gps['lon']), str(gps['lat'])])
                        pylgon = ";".join([' '.join(node) for node in pylgon])
                        # print(pylgon)
                if not pylgon: pylgon = ''

            except Exception as e:
                print(e)

            try:
                csvName = buildName
                name = stripStr(poi.get('name', ''))
                uid = stripStr(poi.get('uid', '')) or ''
                alias = stripStr(poi.get('alias', ''))
                addr = stripStr(poi.get('addr', ''))
                address_norm = stripStr(poi.get('address_norm', ''))
                area = stripStr(poi.get('area', ''))
                area_name = stripStr(poi.get('area_name', ''))
                catalogID = stripStr(poi.get('catalogID', ''))
                di_tag = stripStr(poi.get('di_tag', ''))
                primary_uid = stripStr(poi.get('primary_uid', ''))
                std_tag = stripStr(poi.get('std_tag', ''))
                std_tag_id = stripStr(poi.get('std_tag_id', ''))
                tel = stripStr(poi.get('tel', ''))

                if isinstance(poi.get('x', ''), int):
                    x = poi.get('x', '') / 100
                    y = poi.get('y', '') / 100

                    pointGps = miToGPS(x, y)
                    lon = str(pointGps.get('lon', ''))
                    lat = str(pointGps.get('lat', ''))
                    x = str(x)
                    y = str(y)

                poiInfo.append(",".join(
                    [csvName, name, uid, primary_uid, alias, addr,
                     address_norm, area, area_name, catalogID, di_tag,
                     std_tag, std_tag_id, tel, x, y, lon, lat, pylgon + '\n'])
                )
                print(",".join(
                    [csvName, name, uid, primary_uid, alias, addr,
                     address_norm, area, area_name, catalogID, di_tag,
                     std_tag, std_tag_id, tel, x, y, lon, lat, pylgon + '\n']))

            except Exception as e:
                print(e)

        with open(r'./baidu.csv', mode='a+', encoding='gbk', errors=None) as f:  # 将采集数据写入文件
            f.writelines(poiInfo)



if __name__ == '__main__':
    # 初始化 结果文件表头
    init_csv_title(csvName=r'./baidu.csv')

    nameList = ["水库", "汉中 水库"]

    # 读取关键词
    with open(r'./keywords.csv', mode='r', encoding='gbk', errors=None) as f:  # 读取关键词
        next(f)  # 跳过第一行
        nameList = f.readlines()

    try:
        # 获取实例
        playwright, browser, page = baidu_map_init()

        for name in nameList:
            buildName = name.strip().replace(',', ' ')
            searchPoi(browser, buildName)
            # searchBoxGetPoiInfo(buildName)
            print(buildName)


    finally:
        # 确保关闭浏览器和停止 playwright
        # page.close()
        browser.close()
        playwright.stop()