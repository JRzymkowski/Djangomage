from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import game.mechanics as mechanics

from .models import Game

# Create your views here.
def index(request):

    response = "Log in, continue game, start new game<br>\n"
    response += r'<a href="/game/new">Start new game</a>'

    return HttpResponse(response)

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

        # to be determined by game mechanics
        # cards = []
        # for i in range(6):
        #     cards.append({'id': i, 'name': "B", 'descr': "bbbb bbbbbbbb bbbb bbbbbbb", 'cost': '5 J', 'gain': '3 J'})
        # cards[0] = {'id': 0, 'name': "A", 'descr': "aaa aaaaaa aaa aaa aaaaa", 'cost': '5 P', 'gain': '2 P'}
        #bars = {'yt': 30, 'yw': 20, 'ot': 40, 'ow': 40}

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

        if action != "":
            if ge.is_action_allowed(action):
                message = ge.resolve_action(action)
                if game_object.awaited == "":
                    message += "<br>\n"
                    message += ge.AI_action()
                    ge.gain_resources()
            else:
                message = "Wrong action: " + ge.error_msg
        else:
            # if game_object.awaited != ""
            message = "Choose an action (play or discard a card)"

        cards = ge.get_cards_data()
        bars = ge.determine_bars()

        return render(request, 'game/game_template.html', {'game': game_object, 'message': message, 'cards': cards, 'bars': bars})

    except Exception as err:
        print("Error: " + str(err))
        response += "Game not found"
        return HttpResponse(response)