from django.db import models
import random
import game.mechanics as mechanics
import json
# Create your models here.

class Game(models.Model):
    game_id = models.CharField(max_length=10)
    player_name = models.CharField(max_length=100)
    status = models.IntegerField() # 0 - finished, 1 - ongoing
    winner = models.IntegerField() # 0 - player, 1 - opponent, -1 - none
    active_player = models.IntegerField() # 0 - player, 1 - opponent
    turns_played = models.IntegerField()
    
    # y_ for player's stats, o_ for opponent's stats
    y_tower = models.IntegerField()
    y_wall = models.IntegerField()
    o_tower = models.IntegerField()
    o_wall = models.IntegerField()
    
    y_coffee = models.IntegerField()
    y_javas = models.IntegerField()
    y_mines = models.IntegerField()
    y_rubies = models.IntegerField()
    y_dungeons = models.IntegerField()
    y_pythons = models.IntegerField()

    o_coffee = models.IntegerField()
    o_javas = models.IntegerField()
    o_mines = models.IntegerField()
    o_rubies = models.IntegerField()
    o_dungeons = models.IntegerField()
    o_pythons = models.IntegerField()

    y_cards = models.CharField(max_length=50)
    await = models.CharField(max_length=10)
    after_await = models.CharField(max_length=100)

    y_last_card = models.IntegerField()
    o_last_card = models.IntegerField()

    def initialize(self):
        chars = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        self.game_id = "".join([random.choice(chars) for _ in range(6)])
        self.player_name = "Anonymage"
        self.status = 1 # ongoing
        self.winner = -1 # no winner
        self.active_player = 0 # player
        self.turns_played = 0

        self.y_tower = self.o_tower = 30
        self.y_wall = self.o_wall = 15

        self.y_coffee = self.o_coffee = 1
        self.y_mines = self.o_mines = 1
        self.y_dungeons = self.o_dungeons = 1

        self.y_javas = self.o_javas = 10
        self.y_rubies = self.o_rubies = 10
        self.y_pythons = self.o_pythons = 10

        available_cards = mechanics.cards
        # possibly change to choosing 6 elements from
        y_cards = [random.choice(available_cards)['card_id'] for _ in range(6)]
        self.y_cards = json.dumps(y_cards)
        self.await = ""
        self.after_await = ""

        self.y_last_card = self.o_last_card = -1

        self.save()
    