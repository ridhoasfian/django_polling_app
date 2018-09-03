"""polling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('add_poll/', views.add_poll, name='add_poll'),
    path('edit_poll/<int:polling_id>/', views.edit_poll, name='edit_poll'),
    path('edit_poll/<int:polling_id>/add_choice/', views.add_choice, name='add_choice'),
    path('delete_poll/<int:polling_id>/', views.delete_poll, name='delete_poll'),
    path('edit_choice/<int:choice_id>/', views.edit_choice, name='edit_choice'),
    path('delete_choice/<int:choice_id>/', views.delete_choice, name='delete_choice'),
    path('poll_detail/<int:polling_id>/', views.poll_detail, name='poll_detail'),
    path('poll_vote/<int:polling_id>/', views.poll_vote, name='poll_vote'),
]












#
