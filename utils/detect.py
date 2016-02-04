#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import subprocess
import re
import codecs
import string

def checkPing(iplist, list_length):
	f = open(iplist,"r")
	row = 0

	#results是二维数组，例如[['www.baidu.com',1],[],[],...]
	results = [[0 for col in range(2)] for rows in range(list_length)] 

	#循环操作iplist中每一个ip
	for host in f.readlines():
		if host.startswith("#"): #开头的不算
			continue

		result = ""	#result清空
		#os.system("ping "+host)
		p = subprocess.Popen("ping -n 1 " + host, 
			stdin = subprocess.PIPE, stdout = subprocess.PIPE, 
			stderr = subprocess.PIPE, shell = True)
		out = p.stdout.read()	#out为标准输出
		out = out.decode('gbk')
		#out = out.decode("gbk")
		#以时间分割，取ms前的数值
		#except处理非数值，比如down
		try:
			delay = out.split(u"时间")[1].split("ms")[0][1:]	#delay为字符串
		except:
			result = host[:-1] + "  "
			i = 0
			while (i < (40 - len(host[:-1]))):
				result = result + "*"
				i = i + 1
			results[row][0] = result + "  "
			results[row][1] = "down"
			print (results[row])
			row = row + 1
			continue
		
		#正常的取数值
		result = host[:-1] + "  "
		j = 0
		while (j < (40 - len(host[:-1]))):
			result = result + "*"
			j = j + 1
		results[row][0] = result + "  "
		results[row][1] = float(delay)	#delay字符串转为数值
		print (results[row])
		row = row + 1

	f.close()
	return results

#得到iplist的条数,减去#的3条
def getIPlistLength(iplist):
	return len(open(iplist,'r').readlines()) - 3

def getResults():
	iplist_url = "apps/alive/configs/iplist.txt"	#web用，读取iplist.txt里需要检测的ip列表
	#iplist_url = "../apps/alive/configs/iplist.txt"	#测试用
	if os.path.exists(iplist_url):
		print ("iplist path: " + iplist_url)
		print ("length:%d" %getIPlistLength(iplist_url))
		return checkPing(iplist_url, getIPlistLength(iplist_url))
	else:
		return "Sorry, conf.ini not exist!"

if __name__ == "__main__":
	getResults()
