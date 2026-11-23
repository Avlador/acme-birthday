from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('list/', views.BirthdayListView.as_view(), name='list'),
    path('', views.BirthdayCreateView.as_view(), name='create'),
    

   
]