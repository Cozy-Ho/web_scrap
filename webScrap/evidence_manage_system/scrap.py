from bs4 import BeautifulSoup
from selenium import webdriver
import openpyxl
import time

'''
증거물 관리 시스템 웹 페이지에 통계기능이 없다.
보고서 작성시에 증거물 통계가 필요하여 나에게 준 업무.
서버쪽은 내가 접근할 권한이 없으니 일단 파이썬으로 웹 페이지를 긁어오기로 했다.

셀레니움과 크롬 드라이버를 사용했다.
내 계정으로 로그인을 하고, 보고싶은 페이지를 띄운다. 모바일 or 디스크

데이터 추출 날짜를 설정하고 (다음)버튼을 클릭하며 모든 페이지 내용을 긁어온다.
긁어온 데이터를 evidence_2.xlsx 파일로 저장한다.
엑셀 파일을 보기좋게 정리하여 'evidence_manage.xlsx'로 저장했다.
'''

#---------------------------------------------------------------------------------------
# open page
driver = webdriver.Chrome('C:\\Users\\HEO\\Desktop\\chromdriver\\chromedriver')
driver.get("http://211.248.255.244:8080/wbt/login.jsp")
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
# 로그인 하기
driver.find_element_by_name('UID').send_keys('kj2693119')
driver.find_element_by_name('PASSWORD').send_keys('kangju1379')
# 로그인 버튼 클릭
driver.find_element_by_id('button-1011-btnEl').click()
#---------------------------------------------------------------------------------------

time.sleep(2)

#---------------------------------------------------------------------------------------
#기준 페이지 설정 mobile or disk

# mobile
driver.get("http://211.248.255.244:8080/wbt/evidence/evidence_manage.jsp")
# disk
#driver.get("http://211.248.255.244:8080/wbt/evidence_disk/evidence_disk_manage.jsp")
#---------------------------------------------------------------------------------------


time.sleep(1)

#---------------------------------------------------------------------------------------
# 데이터 추출 날자 설정
# 이것도 mobile 이랑 disk 랑 id가 달라서 바꿔줘야함.

# mobile
driver.find_element_by_id('datefield-1047-inputEl').send_keys('2017-01-01')
driver.find_element_by_id('datefield-1049-inputEl').send_keys('2017-10-31')

#disk
#driver.find_element_by_id('datefield-1046-inputEl').send_keys('2017-01-01')
#driver.find_element_by_id('datefield-1048-inputEl').send_keys('2017-10-31')
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
# 엑셀파일 로딩할때 자꾸 에러나서 찾은 해결책
# 있는 파일 불러오지말고 그냥 객체를 불러와서 데이터 삽입 후 저장 시키는 걸로
wb = openpyxl.Workbook()
sheet = wb.get_sheet_by_name('Sheet')
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
# 페이지를 로딩할때마다 Row를  초기화시키면 계속 덮어쓰기때문에 for문 밖에서 선언
Row = 1
for index in range(0, 12):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # td테그가 표 뿐만아니라 테이블 헤더쪽에도 있어서 데이터가 뭉개짐ㅋ
    # div#~~ 아래에있는 td테그만 긁어오게할것
    # OK 해결. 근데 첫 페이지를 두번긁는데.. 왜지? 데이터가 519개인데 569개이면 정확히 첫페이지를 2번긁은건디..
    my_data = soup.find("div",{"id":"listgrid-body"}).findAll("td")
    count = 1
    Column = 1

    for n in my_data:
        # 15셀당 1줄이기때문에 Row++해줌 & Column 1로 초기화
        if count % 15 == 0:
            Column = 1
            Row += 1
        else:
            sheet.cell(row=Row,column=Column).value = str(n.get_text().strip('\n'))
            Column += 1
        count += 1

    time.sleep(1)

    # 모바일과 디스크 페이지의 다음페이지 버튼 id도 다르다..
    # mobile
    driver.find_element_by_id('button-1038-btnEl').click()
    # disk
    #driver.find_element_by_id('button-1037-btnEl').click()

#---------------------------------------------------------------------------------------
# 엑셀파일로 저장.
wb.save('./evidence_2.xlsx')
