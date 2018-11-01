"""valweb URL Configuration

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

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index, name='index'),
    path('charts/', views.charts, name='charts'),
    path('calendar/', views.calendar, name='calendar'),
    path('money/', views.money, name='money'),
    path('people/', views.people, name='people'),
    path('forms/', views.forms, name='forms'),
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot/', views.forgot, name='forgot'),
    path('submit/', views.submit, name='submit'),
    path('ing/', views.ing, name='ing'),
    path('done/', views.done, name='done'),
    path('download/', views.download, name='download'),
    path('remove/', views.remove, name='remove'),
]
