from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.start_new_game, name='start_new_game'),
    path('game/<slug:game_id>', views.game, name='game')
]