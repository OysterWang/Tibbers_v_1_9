#coding:utf-8
from django.shortcuts import render
from django.http.response import JsonResponse
import socket, time

import utils.trace_thread

'''
#引用例子：points[0]['city']，seq=1为第一跳
points_example = [{
"flag" : 1,
"seq"  : 1,
"city" : "tianjin",
"ip"   : "1.1.1.1",
"coord": [117.20000,39.13333] 
},{
"flag" : 1,
"seq"  : 2,
"city" : "shanghai",
"ip"   : "2.2.2.2",
"coord": [121.48,31.22]
},{
"flag" : 0
}]
'''

#trace首页显示信息
def trace(request):
	host_name = socket.getfqdn(socket.gethostname())	#获取服务器名称
	host_local_ip = socket.gethostbyname(host_name)	#获取服务器ip
	host_internet_ip = "218.24.50.30"	#获取服务器Internet ip
	host_coordinate_lng = 123.8833  #纬度 北京116.432045
	host_coordinate_lat = 41.7 #经度 北京39.910683
	host_city = "Fushun" #Beijing

	point_start={"seq":0, 
	"city":host_city, 
	"host_local_ip":host_local_ip,
	"host_internet_ip":host_internet_ip, 
	"host_coordinate_lng":host_coordinate_lng,
	"host_coordinate_lat":host_coordinate_lat,
	"host_name":host_name
	}

	return render(request, "trace.html", {"point_start":point_start})

#前台jquery不断查询seed_seq的这一跳结果
def ajax_returnPoint(request):
	ip_des = request.GET["ip_des"]
	need_seq = int(request.GET["need_seq"])
	print ("*******************************************************")
	print ("request ip_des: %s, need_seq: %s" %(ip_des,need_seq))
	print ("*******************************************************")

	#开始trace_thread模块的TraceThread进程
	if need_seq == 1:	#第一个请求会开始trace，将记录保存在tmp目录下
		traceThread = utils.trace_thread.TraceThread(ip_des)
		traceThread.start()
		#p1 = Process(target=trace_path, args=(ip_des, need_seq, points))
		#p1.start()
		#p1.join()
		#traceThread = utils.trace_thread.TraceThread(ip_des) #123.125.248.90
		#traceThread.start()

	#sleep一秒后开始trace_thread模块的SeekThread进程
	time.sleep(1)
	seekThread = utils.trace_thread.SeekThread(ip_des, need_seq)
	seekThread.start()
	seekThread.join()	#等待seekThread执行完执行主程序，并return
	'''
	while True:
		try:
			print("############## loop for searching points[%d]" %(need_seq - 1))
			print("####################### found!!! %d:%s"%(need_seq, traceThread.points[need_seq - 1]))
			break
		except Exception as ex:
			print("exception:%s"%ex)
			print("need_seq %d not got yet!"%need_seq)
			time.sleep(0.5)
	'''
	
	print ("\nreturn point:%s" %utils.trace_thread.point_return)	
	return JsonResponse(utils.trace_thread.point_return)	#返回trace_thread模块里的全局变量point_return

def test(request):
	return render(request, "test.html")