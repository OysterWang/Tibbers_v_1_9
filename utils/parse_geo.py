#coding: utf-8
import urllib.request
import re

tmp_geoiptool_html_url = "tmp/geoiptool.html"	#web用
#tmp_geoiptool_html_url = "../tmp/geoiptool.html"	#test用

def parse_geo(ip, seq):
	"""
	此模块根据geoiptool网站，通过请求https://geoiptool.com/zh/?ip=x.x.x.x，得到结果信息页面，再通过正则表达式抽出需要的信息。
	"""
	print("in parse_geo, ip: %s, seq: %s" %(ip, seq))
	regex_ip = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')	#ip正则表达式
	regex_ip_private = re.compile('127[.]0[.]0[.]1|10[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|172[.]((1[6-9])|(2\d)|(3[01]))[.]\d{1,3}[.]\d{1,3}|192[.]168[.]\d{1,3}[.]\d{1,3}')	#私有ip正则表达式

	list_ip = regex_ip.findall(ip)
	list_ip_private = regex_ip_private.findall(ip)
	if len(list_ip) == 0:	#不为ip则返回特殊point
		print ("没有ip，返回空point")
		point = {}
		point["flag"] = 1
		point["seq"] = seq
		point["city"] = "Not known"
		point["ip"] = "*"
		point["coord"] = []
		return point
	if len(list_ip_private) > 0:	#私有ip则返回特殊point
		print ("私有ip，返回空point")
		point = {}
		point["flag"] = 1
		point["seq"] = seq
		point["city"] = "Local"
		point["ip"] = ip
		point["coord"] = []
		return point

	response = urllib.request.urlopen("https://geoiptool.com/zh/?ip=" + ip)
	geo_html = response.read().decode("utf-8")
	#f1 = open(tmp_geoiptool_html_url,"w")
	#f1.write(geo_html)

	#网页正则表达式
	regex_country_name = re.compile(r'<span class="bold">国家:</span>\s*<span>\s*<img src=.*>\s*(.*)\s*</span>')
	regex_country_code = re.compile(r'<span class="bold">国家代码:</span>\s*<span>(.*)</span>')
	regex_district = re.compile(r'<span class="bold">地区:</span>\s*<span>(.*)</span>')
	regex_city = re.compile(r'<span class="bold">城市:</span>\s*<span>(.*)</span>')
	regex_local_time = re.compile(r'<span class="bold">当地时间:</span>\s*<span>(.*)</span>')
	regex_coordinate_lat = re.compile(r'<span class="bold">纬度:</span>\s*<span>(.*)</span>')
	regex_coordinate_lng = re.compile(r'<span class="bold">经度:</span>\s*<span>(.*)</span>')
	
	list_country_name = regex_country_name.findall(geo_html, re.S)
	list_country_code = regex_country_code.findall(geo_html, re.S)
	list_district = regex_district.findall(geo_html, re.S)
	list_city = regex_city.findall(geo_html, re.S)
	list_local_time = regex_local_time.findall(geo_html, re.S)
	list_coordinate_lat = regex_coordinate_lat.findall(geo_html, re.S)
	list_coordinate_lng = regex_coordinate_lng.findall(geo_html, re.S)

	country_name = list_country_name[0]
	country_code = list_country_code[0]
	district = list_district[0]
	city = list_city[0] if list_city[0] else "Not known"
	local_time = list_local_time[0]
	coordinate_lat = list_coordinate_lat[0]
	coordinate_lng = list_coordinate_lng[0]

	print ("ip: %s " %ip)
	print ("country_name: %s" %country_name)
	print ("country_code: %s" %country_code)
	print ("district: %s" %district)
	print ("city: %s" %city)
	print ("local_time: %s" %local_time)
	print ("coordinate_lat: %s" %coordinate_lat)
	print ("coordinate_lng: %s" %coordinate_lng)

	point = {}
	point["flag"] = 1
	point["seq"] = seq
	point["city"] = city
	point["ip"] = ip
	point["coord"] = [float(coordinate_lng), float(coordinate_lat)]

	return point

if __name__ == '__main__':
	parse_geo("10.0.0.1", 3)
	parse_geo("192.168.4.129", 3)
	parse_geo("172.16.0.1", 3)
	parse_geo("61.139.39.73", 3)
