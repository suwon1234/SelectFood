from pyproj import Proj, transform
import pandas as pd
import numpy as np
import pymysql

# DB 연결 설정
DB_HOST = "localhost"
DB_USER = "sf-user"
DB_PW = "A4q8EEdh3c"

# DB 연결
CONNECT = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PW, charset='utf8')
CUR = CONNECT.cursor()

TABLE = pd.read_csv("fulldata_07_24_04_P_일반음식점.csv", encoding="cp949")
TABLE = TABLE.loc[TABLE["영업상태구분코드"] == 1, ["관리번호", "도로명전체주소", "사업장명", "좌표정보(x)", "좌표정보(y)"]]
TABLE = TABLE.replace({'nan': 0})
TABLE = TABLE.replace({np.nan: 0})
TABLE["사업장명"] = TABLE["사업장명"].str.replace("'", "\\'")


ORI = Proj(init='epsg:5174')
DES = Proj(init='epsg:4326')

CONVERTED = transform(ORI, DES, TABLE["좌표정보(x)"].values, TABLE["좌표정보(y)"].values)

CUR.execute("USE SelectFood")

j = 0
for i in CONVERTED[0]:
    TABLE["좌표정보(x)"].values[j] = CONVERTED[1][j]
    TABLE["좌표정보(y)"].values[j] = CONVERTED[0][j]

    command = \
"INSERT IGNORE INTO restaurant \
(관리번호, 사업장명, latitude, longitude) \
VALUES ('{0}', '{1}', {2}, {3})"\
.format(TABLE["관리번호"].values[j], TABLE["사업장명"].values[j], TABLE["좌표정보(x)"].values[j], TABLE["좌표정보(y)"].values[j])
    
    #print(str(j) + " " + command)

    CUR.execute(command)

    j = j + 1

print(TABLE)

CUR.execute("COMMIT")