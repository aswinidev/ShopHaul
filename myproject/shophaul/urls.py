from django.contrib import admin
from django.urls import path
from shophaul import views

urlpatterns = [
    path('',views.index, name="home"),
    path('register',views.userReg, name="register"),
    path('login',views.login,name="login")
]