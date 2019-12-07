from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('detail/', views.detail, name='detail'),
]
