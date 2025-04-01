import requests
import json
import pandas as pd
from lxml import etree
import time
def get_lines(cityE,city):
    lst = []
    for i in range(1,10):
        url ='http://{}.gongjiao.com/lines_{}.html'.format(cityE,i)
        r= requests.get(url).text
        et = etree.HTML(r)
        line = et.xpath('//div[@class="list"]//a/text()')
        for l in line:
            lst.append(l.split(city)[1])
    return lst
def get_dt(city,line):
    url='https://restapi.amap.com/v3/bus/linename?city={}&offset=1&keywords={}&platform=JS&extensions=all&key=624e1a131eb909086c6d1b42fac9ecdf&output=json'.format(city,line)
    r= requests.get(url).text
    rt=json.loads(r)
    try:
        if rt['buslines']:
            print('data available...')
            if len(rt['buslines'])==0:
                print('no data in list...')
            else:
                dt ={}
                dt['line_name']= rt['buslines'][0]['name']
                dt['polyline']= rt['buslines'][0]['polyline']
                dt['total_price']=rt['buslines'][0]['total_price']
                st_name =[]
                st_coords=[]
                for st in rt['buslines'][0]['busstops']:
                    st_name.append(st['name'])
                    st_coords.append(st['location'])
                dt['station_name']= st_name
                dt['station_corrds']= st_coords
                dm = pd.DataFrame([dt])
                print(dm)
                dm.to_csv('./TransportData/{}_lines.csv'.format(cityE),mode='a',header=False)
        else:
            pass
    except:
            print('error... try it again...')
            time.sleep(2)
            get_dt(city,line)
if __name__=="__main__":
    t1 = time.time()
    cityE ='nanjing'
    city ='南京'
    lines_list = get_lines(cityE, city)
    print('{}:有{}条公交线路'.format(city,len(lines_list)))
    for i,line in enumerate(lines_list):
        print('id {}:{}================'.format(i,line))
        get_dt(city, line)
    t2 = time.time()
    print('耗时{}秒'.format(t2 - t1))
    print('ALL DONE!')