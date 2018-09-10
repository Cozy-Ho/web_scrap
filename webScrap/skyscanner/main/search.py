from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import time
import re

'''
호주행 비행기 티켓의 최저가를 알아보기위해 만들어 봤다.
스카이스캐너에서 긁어왔고, 셀레니움 + 크롬 드라이버를 이용했다.
7월 데이터는 'result_1.txt'
8월 데이터는 'result_2.txt'로 저장했다.
'''

#---------------------------------------------------------------------------------------
# open page
def openPage(URL):
    driver.get(URL)
    time.sleep(30)
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
#scrap function
def scrap():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 최저가를 알려주는 테이블의 데이터를 긁어온다.
    datas = soup.findAll("td",{"class":"lowest"})
    #wb = openpyxl.Workbook()
    #sheet = wb.get_sheet_by_name('Sheet')

    file = open("result_2.txt","a+")

    file.write(str(date) + "\n----------\n")
    # 받아온 데이터를 정규식으로 다듬는다.
    for data in datas:
        pattern = re.compile(r"""
        (.*?)?
        (KRW\s)
        (.*?)?
        (<span)
        (.*?)?
        """, re.VERBOSE)
        data = pattern.search(str(data))
        result = data.group(2) + data.group(3)
        file.write(str(result) + "\n")
    file.close()
#---------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------
# main function
driver = webdriver.Chrome('C:\\Users\\HEO\\Desktop\\chromdriver\\chromedriver')
date = 20180801

for i in range(1,32):
    # air_type = 왕복(1) or 편도(0), date만 신경써서 2달치 긁어오면 됨.
    URL = "https://www.travelko.com/locale/ko_KR/flights/list/?air_type=0&slice_info=air.PUS-SYD-" + str(date) + "&adult=1&child=0&infant=0&seat_class=0&d=s&dpt_airport=PUS"
    openPage(URL)
    scrap()
    time.sleep(1)
    date = date+1

driver.close()
#---------------------------------------------------------------------------------------
