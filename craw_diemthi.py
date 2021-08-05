# Chuong trinh tu dong lay ma tinh theo dinh dang
# https://diemthi.mobiedu.vn/search?idStudent=14003463 dinh danhg xxaaaaaa 
# xx ma tinh bat dau tu 01 den 65
# aaaaaa tu 000001 den 999999 tuy so luong
#--------------import thu vien-----------------------------------
import os as OS
import time
from datetime import datetime
import sqlite3 
import keyboard
# import requests
# import unittest
from thuvien_quetdulieudiemthi2021 import maso_format as MSF
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#-------------cac ham phu------------------------------------
class wait_load_data(object):
	def __init__(self,locator,data):
		self.locator = locator
		self.data = data
	def __call__(self,driver):
		element = driver.find_element(*self.locator)
		if self.data == element.text:
			return element
		else:
			return False
class maso_format:

	def __init__(self,fm ="aaxxxx"):
		self.pre = fm.count(fm[0])
		self.end = fm.count(fm[-1])
		self.array= [self.pre,self.end]
		self.len =self.pre + self.end
		if (self.len<len(fm)):
			self.dk = "ERRO"
		else:
			self.dk = "OK"
	def __taochuoi__(self,num, fm):
		if fm == len (str(num)):
			return str(num)
		else:
			return "0"+ self.__taochuoi__(num,fm-1)
	def get(self,*arg):
		if (self.dk =="OK"):
			buff=""
			j=0
			for i in arg:
				if len (str(i))<=self.array[j]:
					buff += self.__taochuoi__(i,self.array[j])
					j+=1
				else: return "NOT_FORMAT"
			return buff
		return "NOT_FORMAT"
def load_data(table,masock,data=['','','','','','','','','','','','',''], datacheck="DATA_LOAD IS GOOD"):
	table.execute("INSERT INTO dulieudiemthi VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(masock,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],datacheck,str((datetime.now())))) 
	return datacheck
def stop_program():
	driver.quit()
	con_data.close()
def save_data(data_b):
	data_b.commit()
	return 0
    # print('{} released'.format(key)) 
start_time = time.time()
maso = maso_format("xxaaaaaa")
options = Options()
options.add_argument("--window-size=800,800")
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--window-size=1400x1080")
options.add_argument("--mute-audio")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
con_data = sqlite3.connect("dulieudiemthi2021.db")
cur_data = con_data.cursor()
sql_command = "CREATE TABLE IF NOT EXISTS dulieudiemthi (sobaodanhck ,sobaodanh,cumthi,toan,nguvan,ngoaingu,vatly,hoahoc,sinhhoc,dtbtunhien,lichsu,diali,gdcd,dtbxahoi,datacheck,time_load DATETIME)"
cur_data.execute(sql_command)
data_buff=[]
error_num=[]
STOP_PRO = False
DATA_LOAD_ERROR_COUNT=0
DATA_LOAD_COUNT = 0
DATA_SAVE_CYCLE =8
DATA_CHECK = "DATA_LOAD IS GOOD"
KEY=''
cur_data.execute("select * from dulieudiemthi order by sobaodanhck desc")
result = cur_data.fetchone()
if result:
	MASO_MAX= result[0]
else: MASO_MAX="01000000"
print ("MA SO DU THI DA TAI HIEN TAI: %s" %(MASO_MAX))
print(result)
key  = input(" Enter (tiep tuc)/ Nhap 'x' (thoat): " )
if (key == "x" ) or (key == "X" ) :
	con_data.close()
	exit()
START_MT= int(MASO_MAX[:2])
END_MT =66
START_STT = int(MASO_MAX[2:])+1
END_STT=	1000000
DRIVER_PATH = OS.getcwd()+"\\chromedriver"
driver  = webdriver.Chrome(options=options,executable_path = DRIVER_PATH)
driver.get("http://diemthi.mobiedu.vn/")
#----------------------------------------------------------------------
print("-----------------BAT DAU LUC: "+ str( datetime.now())+"-----------------------------")
start_time='0'
for matinh in range(START_MT,END_MT):
	if STOP_PRO:
		break
	for sott in range(START_STT,END_STT):
		MASODUTHI = maso.get(matinh,sott)
		try:
			elem = driver.find_element_by_class_name("inp")
			elem.clear()
			elem.send_keys(MASODUTHI)
			driver.find_element_by_xpath("//button[@class ='btn btn-search']").click()
			elem = WebDriverWait(driver,5).until(wait_load_data((By.XPATH,"//table/tbody/tr/td[1]"),MASODUTHI))
			DATA_CHECK = load_data(cur_data, MASODUTHI,[x.text for x in driver.find_elements(By.XPATH,"//table/tbody/tr/td")],datacheck="LOAD DATA IS GOOD")
			con_data.commit()
			DATA_LOAD_ERROR_COUNT =0
		except:
			try:
				if driver.find_element_by_xpath("//div[@class ='error text-danger']").text == "Chưa có dữ liệu điểm thi cho số báo danh này" :
					DATA_LOAD_ERROR_COUNT+=1
					DATA_CHECK = load_data(cur_data, MASODUTHI,datacheck="LOAD DATA IS ERRO")
					con_data.commit()
					if DATA_LOAD_ERROR_COUNT>4:
						DATA_LOAD_ERROR_COUNT =0
						break	
				else:

					DATA_CHECK= load_data(cur_data, MASODUTHI,datacheck= "LOAD DATA IS ERRO")
					con_data.commit()
			except: 
				DATA_CHECK= load_data(cur_data, MASODUTHI,datacheck="LOAD DATA IS ERRO")
				con_data.commit()
		if DATA_LOAD_COUNT == DATA_SAVE_CYCLE:
			DATA_LOAD_COUNT =save_data(con_data)
		print(MASODUTHI +"------"+DATA_CHECK+"-------"+str(datetime.now()), end ="\r")

		if keyboard.is_pressed("x"):
			STOP_PRO = True
			break
		elif keyboard.is_pressed("p") :
			print("\n+ PAUSE+ NHAP 'C' DE TIEP TUC ")
			while True:
				if keyboard.is_pressed("c"):
					break
	con_data.commit()
con_data.commit()
stop_program()
print(datetime.now())
