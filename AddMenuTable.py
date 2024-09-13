from pyproj import Proj, transform
import pandas as pd
import numpy as np
import pymysql
import requests
import asyncio
import json
import threading
import multiprocessing

# DB 연결 설정
DB_HOST = "localhost"
DB_USER = "sf-user"
DB_PW = "A4q8EEdh3c"

# DB 연결
CONNECT = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PW, charset='utf8')
CURSOR = CONNECT.cursor()

def getMenu(Name: str):
    uri = "https://www.happytanuki.kr/GetMenusByName?Name=" + Name

    print("\033[33m" + Name + "\033[0m" + " " + json.dumps(requests.get(uri).json(), ensure_ascii=False))

def listStrip(myList: list):
    ReturnValue = list()

    for item in myList:
        ReturnValue.append(item[1])
    
    return ReturnValue

def main():
    asyncobject = list()

    print("\033[33m" + "Getting Names.." + "\033[0m")

    CURSOR.execute("USE SelectFood")
    CURSOR.execute("Select 관리번호, 사업장명, \
                (6371 * ACos(Cos(Radians(latitude)) * Cos(Radians(37.2092017)) * Cos(Radians(126.9769365) - Radians(longitude)) + Sin(Radians(latitude)) * Sin(Radians(37.2092017)))) as Distance \
                    From restaurant \
                    Having Distance <= 50 \
                    Order By Distance ASC;")

    RESTAURANTS = CURSOR.fetchall()

    print("\033[33m" + "Complete." + "\033[0m")
    print("\033[33m" + "Process pool executing.." + "\033[0m")

    processPool = multiprocessing.Pool(5)
    processPool.map(getMenu, listStrip(RESTAURANTS))
    processPool.close()
    processPool.join()

    # for RESTAURANT in RESTAURANTS:
    #     getterThread = multiprocessing.Process(target=getMenu, args=(RESTAURANT[0], ))
    #     asyncobject.append(getterThread)

    # print("\033[33m" + "Complete." + "\033[0m")

    # for page in range(0, len(asyncobject), 5):
    #     print("\033[33m" + "Executing Thread( " + str(page + 5) + " / " + str(len(asyncobject)) + " )(" + str((page + 5)/len(asyncobject)*100) + "%).." + "\033[0m")
    #     for thread in asyncobject[page:page+5]:
    #         thread.start()

    #     print("\033[33m" + "Waithing for threads to complete.." + "\033[0m")
    #     for thread in asyncobject[page:page+5]:
    #         thread.join()

    CURSOR.close()
    CONNECT.close()

if __name__ == "__main__":
    main()