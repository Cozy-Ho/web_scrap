from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver
import openpyxl
import requests
import re


# nogada.py를 돌리고 난 뒤, 가격 데이터를 엑셀파일에 작성하는 함수.


wb = openpyxl.load_workbook('data/20171016_휴대폰추가구매_모델리스트.xlsx')
sheet = wb.get_sheet_by_name('Mobile')


data_file = open('result.txt','r')

for rowNum in range (4, 220):
	sheet.cell(row=rowNum, column=8).value = data_file.readline()

wb.save('./updated.xlsx')

data_file.close()
