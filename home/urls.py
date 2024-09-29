from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.RoomHomeView.as_view(), name='home'),
    path('new/', views.RoomCreateView.as_view(), name='new_room'),
    path('list/', views.RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('room/reserve/<int:pk>/', views.ReservationCreateView.as_view(), name='reservation'),
    path('room/modify/<int:pk>/', views.RoomEditView.as_view(), name='update_room'),
    path('room/delete/<int:pk>/', views.RoomDeleteView.as_view(), name='remove_room'),
]
