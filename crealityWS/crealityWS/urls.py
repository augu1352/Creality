"""crealityWS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crealityAPP.urls')),
    path('videos/', include('videostream.urls')),
]





# from django.views.generic.simple import direct_to_template
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
# urlpatterns += patterns("",(r"^$", direct_to_template, {"template": "home/index.html"}))


#Intro URL






# wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
