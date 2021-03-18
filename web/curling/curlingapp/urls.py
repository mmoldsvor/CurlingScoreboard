from django.contrib import admin
from django.urls import path
from . import views #Relativ import av viewsfunksjonen

appname = "curlingapp"
urlpatterns = [
    path('<str:match>/', views.match, name='match'),
    path('sendPos/<str:match>/', views.send_pos, name='send_pos'),
]