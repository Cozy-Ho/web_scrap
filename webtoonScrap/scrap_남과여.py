from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import shutil
import time
import re

'''
삽질끝에 성공..
원래 bs4로 그냥 긁어오려했는데 긁어오려는 페이지에서 봇 접근을 막아놨다.
셀레늄으로 가져와서 저장하려고 하니까 또 HTTP403 에러;;
그래서 requests 라이브러리와 file 이용해서 저장.
일단 이미지 src 값만 다 긁어서 파일로 저장한 뒤에
이미지를 하나하나 저장하는 방법을 이용했다.
'''

# 웹에서 링크 긁어오기부터.
#------------------------------------------------------------------------------------
driver = webdriver.Chrome("C:\\git\\web_scrap\\chromedriver")

count = 1
# 총 58화, 10화 미만일때는 01, 02, 03... 이런식이라 if로 나눠줌.
for i in range(0,57):
    if count < 10:
        driver.get("https://webtoon.bamtoki.com/%EB%82%A8%EA%B3%BC-%EC%97%AC-0" + str(count) + ".html")
    else:
        driver.get("https://webtoon.bamtoki.com/%EB%82%A8%EA%B3%BC-%EC%97%AC-" + str(count) + ".html")
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    time.sleep(3)

    # 파일에 src값 저장하기.
    with open("srclist.txt", 'a+') as f:
        for link in bs.findAll("img", src=re.compile("^(https://ie.bamtoki)")):
            result = re.search('src=\"(.*?)\"', str(link))
            f.write(result.group(1) + "\n")

    count += 1
#------------------------------------------------------------------------------------
