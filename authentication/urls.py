from django.urls import path, include
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='home'),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registration, name="register")
]