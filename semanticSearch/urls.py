from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('searchbooking/', views.search_booking, name='search_booking'),
    path('searchmenuitem/', views.search_menu_item, name='search_menu_item'),
    path('searchemployee/', views.search_employee, name='search_employee'),
]