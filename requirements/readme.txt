相关信息：
1.
百度地图api
http://api.map.baidu.com/api?v=2.0&ak=91fcUGbvXDaGq9Bmhzfj2GOb

*******************************************************************

"""
E:\CloudSync\LITB_NETWORK_SYNC\Python_Projects\Tibbers\utils>tracert -d www.baidu.com

通过最多 30 个跃点跟踪
到 www.a.shifen.com [61.135.169.121] 的路由:

  1    <1 毫秒    2 ms     1 ms  192.168.4.129
  2    <1 毫秒   <1 毫秒   <1 毫秒 192.168.11.30
  3     2 ms     2 ms     2 ms  202.106.57.169
  4     1 ms     3 ms     2 ms  61.148.155.77
  5     5 ms     3 ms     3 ms  61.148.146.29
  6     3 ms     2 ms     2 ms  124.65.58.174
  7     2 ms     3 ms     4 ms  123.125.248.90
  8     *        *        *     请求超时。
  9     2 ms     1 ms     1 ms  61.135.169.121

跟踪完成。

E:\CloudSync\LITB_NETWORK_SYNC\Python_Projects\Tibbers\utils>

points = [{
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
"""

******************************************************************
Django notes
1.  Django安装
python version 3.4.3，django安装：
cd Django-1.8.3
python setup.py install

2.  创建project
在目录E:\CloudSync\LITB_NETWORK_SYNC\Python_Projects 下，创建项目Tibbers：
django-admin startproject Tibbers
注：
不知道为啥环境变量不生效，只能写全路径创建：
D:\Python34\Lib\site-packages\Django-1.8.3-py3.4.egg\django\bin\django-admin startproject Tibbers

3.  创建app
Tibbers相关目录下，创建app：
django-admin startapp testmap
注：
D:\Python34\Lib\site-packages\Django-1.8.3-py3.4.egg\django\bin\django-admin startapp testmap

4.  修改settings.py
配置app，并增加引用静态文件（如js、css、image等，在应用testmap下新建static/js/jquert-1.11.3.js即可以访问）。
vi Tibbers/settings.py：
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#自定义应用
    'testmap',
)

STATIC_URL = '/static/'
#引用静态文件（如js、css、image等）新加入
HERE_PATH=os.path.dirname(__file__) 
STATICFILES_DIRS = ( 
 os.path.join(HERE_PATH,"static").replace('\\','/'),
)

5.  修改urls.py
vi Tibbers/Tibbers/urls.py：
#引用static新加入
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#http://localhost:8000/ajax_returnPoint?ip_des=1.1.1.1
urlpatterns = [
    url(r'^$', 'testmap.views.index', name='index'),	#新加首页
    url(r'^ajax_returnPoint/$', 'testmap.views.ajax_returnPoint', name='ajax_returnPoint'),	#新加自定义函数
    url(r'^admin/', include(admin.site.urls)),  
]

#引用static新加
urlpatterns += staticfiles_urlpatterns()

6.  编写views.py
vim Tibbers/testmap/views.py：
#引入相关模块
from django.shortcuts import render
from django.http.response import JsonResponse

#request是必须的,host_name等字典是参数。在Tibbers/testmap/templates创建index.html，可在html页面引用{{host_name}}
def index(request):
	return render(request, "index.html", {"host_name":host_name, "host_local_ip":host_local_ip,})

def ajax_returnPoint(request):
	ip_des = request.GET["ip_des"]	#传来的参数ip_des
	return JsonResponse("point")

7.  启动服务
启动服务器，默认端口8000
cd /d E:\CloudSync\LITB_NETWORK_SYNC\Python_Projects\Tibbers
python manage.py runserver

