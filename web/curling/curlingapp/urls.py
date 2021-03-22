from django.contrib import admin
from django.urls import path
from . import views #Relativ import av viewsfunksjonen

appname = "curlingapp"
urlpatterns = [
    path('<str:match>/', views.live, name='live'),
    path('<str:match>/<int:end>/<int:throw>/', views.past, name='past'),
    path('sendPos/<int:camId>/', views.send_pos, name='send_pos'),
    path('', views.matches, name='matches'),

]