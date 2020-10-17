"""belt_exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from belt_examApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('add', views.add_trip),
    path('create_trip', views.create_trip),
    path('view_trip/<int:tripid>', views.view_trip),
    path('join/<int:tripid>', views.join_trip),
    path('del/<int:tripid>', views.del_trip),
    path('unjoin/<int:tripid>', views.unjoin),
    path('edit/<int:tripid>', views.edit),
    path('update<int:tripid>', views.update),
]
