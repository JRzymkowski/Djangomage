from django.shortcuts import render
from django.http import HttpResponse

from .models import Game

# Create your views here.
def index(request):
    return HttpResponse("Log in, continue game, start new game")

def game(request, game_id):
    return HttpResponse("Game view for game " + game_id)