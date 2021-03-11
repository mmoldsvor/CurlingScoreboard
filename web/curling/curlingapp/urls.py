from django.contrib import admin
from django.urls import path
from . import views #Relativ import av viewsfunksjonen

appname = "curlingapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('sendPos/', views.send_pos, name='send_pos'),
]