from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/<slug:game_id>', views.game, name='game')
]