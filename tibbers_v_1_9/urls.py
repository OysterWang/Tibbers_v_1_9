"""tibbers_v_1_9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tib_apps.tib_trace import views as tib_trace_views

#引用static新加入
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^$',tib_trace_views.test),
    url(r'^trace$', tib_trace_views.trace), 
    url(r'^ajax_returnPoint/$', tib_trace_views.ajax_returnPoint),
    #url(r'^alive',tib_trace_views.index,name='alive'),
    url(r'^admin/', admin.site.urls),
]

#引用static新加
urlpatterns += staticfiles_urlpatterns()