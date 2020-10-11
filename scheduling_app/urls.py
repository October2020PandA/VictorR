from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.log),
    path('home' , views.home),
    path('logout', views.log_out),
    path('add_date', views.add_date),
    path('remove/<int:id>', views.remove_date),
    path('edit/<int:id>', views.edit_page),
    path('edit_date/<int:id>', views.edit_date),
    path('confirm_page/<int:id>', views.confirm_page),
    path('confirm/<int:id>', views.confirm),
    path('un-confirm/<int:id>', views.un_confirm),
    path('prev_mo/<int:id>', views.home),
    # path('next_mo', views.next_month),
]