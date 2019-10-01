from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import game.mechanics as mechanics

from .models import Game

import traceback

# Create your views here.
def index(request):

    response = "Log in, continue game, start new game<br>\n"
    response += r'<a href="/game/new">Start new game</a>'

    return render(request, 'game/index.html')

def start_new_game(request):
    new_game = Game()
    new_game.initialize()
    game_id = new_game.game_id

    return HttpResponseRedirect(reverse('game:game', args = (game_id,)))

def game(request, game_id):
    response = "Game view for game " + game_id + "<br>\n"

    try:
        game_object = Game.objects.get(game_id = game_id)
        message = "Showing current game state"

        ge = mechanics.GameEngine(game_object)
        chosen_card = None
        chosen_action = ""
        action = ""

        if request.POST:
            for i in range(6):
                name = 'card' + str(i)
                if name in request.POST:
                    chosen_card = i
                    if request.POST[name] == "Play":
                        chosen_action = "P"
                    elif request.POST[name] == "Discard":
                        chosen_action = "D"

            action = chosen_action + str(chosen_card)

        if action != "" and game_object.status != 0:
            if ge.is_action_allowed(action):
                message = ge.resolve_action(action)
                if game_object.awaited == "":
                    message += "<br>\n"
                    message += ge.AI_action()
                    ge.gain_resources()
            else:
                message = "Wrong action: " + ge.error_msg

            game_object.winner, game_object.status = ge.status()
        else:
            # if game_object.awaited != ""
            message = "Choose an action (play or discard a card)"

        if game_object.status == 0:
            message = "Game finished. "
            if game_object.winner == 0:
                message += "You won"
            elif game_object.winner == 1:
                message += "You lost"

        cards = ge.get_cards_data()
        bars = ge.determine_bars()
        game_object.save()


        return render(request, 'game/game_template.html', {'game': game_object, 'message': message, 'cards': cards, 'bars': bars})

    except Exception as err:
        print(traceback.format_exc())
        print("Error: " + str(err))
        response += "Game not found"
        return HttpResponse(response)