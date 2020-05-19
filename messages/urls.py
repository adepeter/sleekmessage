from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_chats, name='list_chats'),
    path('<slug:user>/compose/', views.start_chat, name='start_chat'),
    path('<int:id>/', views.read_chat, name='read_chat'),
    path('<int:id>/<slug:user>/', views.read_chat, name='read_chat'),
]
