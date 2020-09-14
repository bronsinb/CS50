from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/<str:hotel_name>', views.hotel_rooms, name='hotel_rooms'),
    path('hotels', views.hotels, name='hotels'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API
    path("api/rooms", views.rooms, name="api_rooms"),
    path("rooms/api/rooms", views.rooms, name="room_api_rooms"),
]