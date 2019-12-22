"""sithsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import mainapp.views as mainapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.main, name='main'),
    path('profile/', mainapp.profile, name='profile'),
    path('add_task/<int:pk>', mainapp.add_task, name='add_task'),
    path('test/<int:pk>', mainapp.test, name='test'),
    path('info/<int:pk>', mainapp.info, name='info'),
    path('quiz/<int:pk>', mainapp.quiz, name='quiz'),
    path('sith/', mainapp.SithList.as_view(), name='sith_list'),
    path('sith/<int:pk>', mainapp.SithDetail.as_view(), name='shadows'),
    path('select/<int:master>/<int:pk>', mainapp.select, name='select'),
]
