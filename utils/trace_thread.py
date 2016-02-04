#coding:utf-8
import threading
import time, re
from subprocess import Popen, PIPE

import utils.parse_geo
import utils.parse_ipinfo

"""
此模块有两个进程TraceThread和SeekThread。
TraceThread用于need_seq=1时，开始trace并保存结果到txt
SeekThread用于不断读取txt中需要的行，并取出ip，根据ip查找相应信息并组成point字典，views中根据前台查询返回全局变量point_return

point_return = {
"flag" : 1,
"seq"  : 1,
"city" : "tianjin",
"ip"   : "1.1.1.1",
"coord": [117.20000,39.13333]
}
point_return = {
"flag" : 0
}
"""
point_return = {}	#全局变量，用于保存返回前台的结果point

def tmp_trace_txt_url(domain_str):
	"""
	ThraceThread进程的trace结果保存路径
	Args:
	domain_str:要trace的域名或ip，用于组成txt文件名，名称规则trace_要trace的域名或ip
	"""
	tmp_trace_txt_url = "tmp/trace_"	#web用
	#tmp_trace_txt_url = "../tmp/trace_"	#测试用
	return tmp_trace_txt_url + domain_str + ".txt"

class TraceThread(threading.Thread):
	"""
	TraceThread用于need_seq=1时，开始trace并保存结果到txt
	"""
	def __init__(self, domain_str):
		"""
		Args:
		domain_str:要trace的域名或ip
		"""
		threading.Thread.__init__(self)
		self.domain_str = domain_str
		self.cmd_str = "tracert -d " + self.domain_str
		self.ip_list = []
		self.regex_ip = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')	#正则表达式：含有ip或者至少一个*的行
		print("%s created!" %self.getName())
		print("%s cmd_str : %s"%(self.getName(), self.cmd_str))
		self.trace_txt = open(tmp_trace_txt_url(self.domain_str),"w")	#保存trace结果的txt

	def trace_extract_save(self):
		"""
		含有ip或者至少一个*的行要保存到txt中
		"""
		p = Popen(self.cmd_str, stdout=PIPE)
		num = 0
		while True:
			one_line = p.stdout.readline()
			if not one_line:
		   		break
			ip_extract = self.regex_ip.findall(one_line.decode('gbk'))	#抽出含有ip或者至少一个*的行
			if len(ip_extract) >= 1:
				num += 1
				self.trace_txt.write(one_line.decode('gbk').strip("\n"))	#oneline存入txt中
				self.trace_txt.flush()
				#print("%s : write line[%d] ip:%s  %s" %(self.getName(), num, ip_extract[0], one_line))			
		self.trace_txt.close()
		
	def run(self):
		self.trace_extract_save()
		print ("%s-tracert %s end!"%(self.getName(), self.domain_str))
		print ("%s over" %self.getName())

class SeekThread(threading.Thread):
	"""
	SeekThread用于不断读取txt中需要的行，并取出ip，根据ip查找相应信息并组成point字典，views中根据前台查询返回全局变量point_return
	"""
	def __init__(self, domain_str, need_seq):
		"""
		Args:
		domain_str:要trace的域名或ip
		need_seq:当前需要的hop数
		"""
		threading.Thread.__init__(self)
		self.domain_str = domain_str
		self.need_seq = need_seq
		self.target_ip = ""
		self.ip_list = []	#保存已经遍历过的ip，每次打开txt都初始化
		self.regex_ip = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')	#正则表达式：含有ip或者至少一个*的行
		print("******%s created. Need lines[%d]" %(self.getName(), self.need_seq))
	
	def seekSeq(self):
		loop_time = 1	#循环读取关闭txt的次数
		global point_return
		point_return = {}
		while True:	#循环读取关闭txt
			time.sleep(1)
			self.trace_txt = open(tmp_trace_txt_url(self.domain_str),"r")	#要读取的txt
			print("******%s the %d time open txt to seek lines[%d]" %(self.getName(), loop_time, self.need_seq))
			loop_time += 1
			flag = 0	#读取到的line是第几行，每次打开txt都初始化
			self.ip_list = []	#本次读取txt取出的list列表，每次打开txt都初始化

			try:
				while True:
					line = self.trace_txt.readline()
					
					print("******%s flag: %d origin line: %s" %(self.getName(), flag, line))
					if not line:
						#没有line了：检查是否已经trace完，判断上一个seq请求的是否已经是target_ip
						print("******%s not line, need check , len(self.ip_list) = %d" %(self.getName(), len(self.ip_list)))
						if self.ip_list[len(self.ip_list) - 1] == self.target_ip:	#上个seq请求已经trace完毕，则设置point_return的flag=0
							point_return['flag'] = 0
							print("******%s already to the last hop" %(self.getName()))
							print("******%s make it into point_return: %s" %(self.getName(), point_return))
							return
						break	#否则没有trace完毕，重新open txt

					#读取到line，做出处理
					if flag == 0:	#若此行是第一行，读取ip为target_ip，继续读取下一行
						ip_extract = self.regex_ip.findall(line)
						self.target_ip = ip_extract[0]
						flag += 1
						#print("******%s line[0]: %s" %(self.getName(), line))
						#print("******%s target_ip: %s" %(self.getName(), self.target_ip))
						continue
					else:	#此行不是第一行
						if self.need_seq == flag:	#flag如果到了need_seq行，就取出ip，并组装字典
							print("******%s line[%d/%d]: %s" %(self.getName(), flag, self.need_seq, line))
							ip_extract = self.regex_ip.findall(line)
							if len(ip_extract) >= 1:
								#有两种方法得到字典point_return：parse_geo模块和parse_ipinfo模块，两个模块调用的网站不同。geo是网页抓取，ipinfo是api返回json。任选一种。
								#point_return = utils.parse_geo.parse_geo(ip_extract[0], self.need_seq)	#geo tool
								point_return = utils.parse_ipinfo.parse_ipinfo(ip_extract[0], self.need_seq)	#ipinfo tool
								self.ip_list.append(ip_extract[0])
								print("******%s find lines[%d]: %s  %s"%(self.getName(), self.need_seq, ip_extract[0], line))
								print("******%s make it into point_return: %s" %(self.getName(), point_return))
								print("******%s len(self.ip_list) = %d" %(self.getName(), len(self.ip_list)))
								return
						else:	#flag未到need_seq行，ip加入list，继续读取下一行
							print("******%s not yet line[%d/%d]: %s" %(self.getName(), flag, self.need_seq, line))
							ip_extract = self.regex_ip.findall(line)
							if len(ip_extract) >= 1:
								self.ip_list.append(ip_extract[0])
							flag += 1
							continue
			except Exception as ex:
				print("******%s Exception: %s" %(self.getName(), ex))
				continue	#重新open txt

	def run(self):
		self.seekSeq()
		print ("******%s over" %self.getName())

if __name__ == "__main__":
	traceThread = TraceThread("www.baidu.com")
	traceThread.start()
	time.sleep(1)
	seekThread = SeekThread("www.baidu.com", 3)
	seekThread.start()
	time.sleep(10)
	print("I need%s" %point_return)
