from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.home_page),
    path('register/',views.register),
    path('login/',views.login),
    path('update/',views.update),
    path('logout/',views.logout),
    path('set_cookie/',views.set_cookie),
]