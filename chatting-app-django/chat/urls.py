from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
    path('logout/', views.out, name='logout'),
    path('land/', views.land, name='land'),
    path('register/', views.register_view, name='register')
]
