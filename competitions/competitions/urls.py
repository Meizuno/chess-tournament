"""
URL configuration for competitions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('tournaments/', tournaments_page, name='tournaments'),
    path('tournaments/new/', new_tournament_page, name='new_tournament'),
    path('tournaments/<str:tournament_unique_id>/', tournament_detail_page, name="tournament_detail"),
    path('tournaments/<str:tournament_unique_id>/edit/', tournament_edit_page, name="tournament_edit"),
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),
    path('profile/<str:player_unique_id>/', profile_page, name='profile'),
    path('profile/<str:player_unique_id>/edit/', profile_edit, name='profile_edit'),
    path('api/tournaments/', TournamentView.as_view()),
    path('api/tournaments/<str:tournament_unique_id>/', TournamentDetailView.as_view()),
    path('api/profile/<str:player_unique_id>/', PlayerDetailView.as_view()),
]
