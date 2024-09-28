from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.RoomHomeView.as_view(), name='home'),
    path('new/', views.RoomCreateView.as_view(), name='new_room'),
]
