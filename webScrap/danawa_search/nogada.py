from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver
import openpyxl
import requests
import re
import time

'''
연구용 모바일 기기 구매 계획서 작성을 위해 맡긴 업무.
보유하고있지 않은 새로운 모델 리스트 '20171016_휴대폰추가구매_모델리스트.xlsx'에서 모델명을 추출해 'data.txt'파일로 저장한다.
저장한 데이터를 중복을 제거하여 setted_data.txt로 저장.

다나와 사이트에서 모델명으로 검색을 한다.
최고가를 적어달라 요구하였으므로, 가격이 높은 순서대로 정렬후 긁어왔다.
긁어온 가격 데이터는 'result.txt'에 저장했다.
'''

#--------------------------------------------------------------------------------------------
#순서 유지 & 중복 제거함수
def remove_duplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res
#--------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
# 엑셀파일에서 모델명을 뽑아 data.txt파일로 저장.
wb = openpyxl.load_workbook('data/20171016_휴대폰추가구매_모델리스트.xlsx')
sheet = wb.get_sheet_by_name('Mobile')

my_file = open('./data.txt', 'w')
my_file.write("\n")

# 4번째 열 = 모델명
for i in range(4, 219):
    my_file.write(sheet.cell(row=i, column=4).value + "\n")
my_file.close()

#--------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
# 리스트 중복제거

# 데이터를 읽어들임
my_data = open('data.txt','r')
# 줄바꿈을 기준으로 데이터 입력
set_data = my_data.read().split("\n")

setted_data = remove_duplicates(set_data)

setdata = open('setted_data.txt','w')

for i in setted_data:
    setdata.write(i+"\n")

setdata.close()
#--------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
# data.txt파일을 이용해 검색. 다나와 사이트에서 일괄 검색.
driver = webdriver.Chrome('C:\\Users\\HEO\\Desktop\\chromdriver\\chromedriver')
driver.get("http://www.danawa.com/")

my_data.readline()

result_data = open('result.txt','a+')
#--------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
# 검색결과를 엑셀파일에 입력 & 다음데이터 검색. 데이터 개수만큼 반복.
for n in range(0, 140):
    line = my_data.readline()
    # 검색창 ID
    driver.find_element_by_id('AKCSearch').send_keys('%s' % line)
    time.sleep(4)
    # 가격기준 내림차순 버튼. 최고가 검색용.
    driver.find_element_by_id('priceDESC').click()
    time.sleep(2)

    # 버튼을 누른 후의 페이지 소스를 받아옴.
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #가격 텍스트를 공백제거후 저장.
    result = (soup.find("",{"class":"price_sect"}).get_text().strip())
    result_data.write(result+"\n")

    time.sleep(1)

    #재검색을위해 홈페이지로 이동.
    driver.get("http://www.danawa.com")
#--------------------------------------------------------------------------------------------

my_data.close()
result_data.close()
