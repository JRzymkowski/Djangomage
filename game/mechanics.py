import json
from random import choice

# placeholder cards for testing
# awaited can have single action/number pair
# cost and discard can affect only one resource type
# gain to your coffeehouse, mines or dungeons always is the first effect
# effects should always have +/- sign
CARDS = (
    {'card_id': 0, 'name': "Sneaky attack", 'description': "5 damage to opponent's wall", 'effects': "o_wall,-5", 'awaited': "",
     'eff_after_awaited': "", 'cost': "5 P", 'gain': "1 P"},
    {'card_id': 1, 'name': "Stonemasons", 'description': "Your wall gain 7", 'effects': "y_wall,+7", 'awaited': "",
     'eff_after_awaited': "", 'cost': "5 J", 'gain': "1 J"},
    {'card_id': 2, 'name': "Bookkeeping", 'description': "Discard two cards", 'effects': "",
     'awaited': "D2", 'eff_after_awaited': "", 'cost': "5 R", 'gain': "1 J"},
    {'card_id': 3, 'name': "Extra scaffolding", 'description': "Your wall gain 15", 'effects': "y_wall,+15",
     'awaited': "", 'eff_after_awaited': "", 'cost': "10 J", 'gain': "1 J"},
    {'card_id': 4, 'name': "New coffee machine", 'description': "Your gain one coffeehouse", 'effects': "y_coffee,+1",
     'awaited': "", 'eff_after_awaited': "", 'cost': "7 R", 'gain': "1 R"},
    {'card_id': 5, 'name': "Better pickaxes", 'description': "Your gain one mine", 'effects': "y_mines,+1",
     'awaited': "", 'eff_after_awaited': "", 'cost': "8 P", 'gain': "2 P"},
    {'card_id': 6, 'name': "Deeper dungeons", 'description': "Your gain one dungeon", 'effects': "y_dungeons,+1",
     'awaited': "", 'eff_after_awaited': "", 'cost': "5 J", 'gain': "2 J"},
    {'card_id': 7, 'name': "Mutual destruction", 'description': "10 damage to opponent, 5 damage to you", 'effects': "o_wall,-10;y_wall,-5",
     'awaited': "", 'eff_after_awaited': "", 'cost': "10 P", 'gain': "1 P"},
    {'card_id': 8, 'name': "Prism", 'description': "Gain 5 rubies and discard one card", 'effects': "y_rubies,+5",
     'awaited': "D1", 'eff_after_awaited': "", 'cost': "6 J", 'gain': "1 J"},
    {'card_id': 9, 'name': "Snake attack", 'description': "4 damage to opponent's tower", 'effects': "o_tower,-4",
     'awaited': "", 'eff_after_awaited': "", 'cost': "6 P", 'gain': "1 J"},
    {'card_id': 10, 'name': "Bountiful harvest", 'description': "You and the opponent gain one coffeehouse",
     'effects': "y_coffee,+1;o_coffee,+1", 'awaited': "", 'eff_after_awaited': "", 'cost': "7 J", 'gain': "1 J"},
    {'card_id': 11, 'name': "Earthquake", 'description': "You and the opponent lose one mine",
     'effects': "y_mines,-1;o_mines,-1", 'awaited': "", 'eff_after_awaited': "", 'cost': "5 P", 'gain': "2 R"},
    {'card_id': 12, 'name': "Free stuff", 'description': "Gain 5 javas and 5 rubies",
     'effects': "y_javas,+5;y_rubies,+5", 'awaited': "", 'eff_after_awaited': "", 'cost': "3 P", 'gain': "2 R"},
    {'card_id': 13, 'name': "Extreme digging", 'description': "Gain 2 mines",
     'effects': "y_mines,+2", 'awaited': "", 'eff_after_awaited': "", 'cost': "11 J", 'gain': "2 R"},
    {'card_id': 14, 'name': "Rot", 'description': "You lose 3 javas, opponent loses 10 javas",
     'effects': "o_javas,-10;y_javas,-3", 'awaited': "", 'eff_after_awaited': "", 'cost': "7 R", 'gain': "2 J"},
    {'card_id': 15, 'name': "Fortifications", 'description': "You gain 8 wall",
     'effects': "y_wall,+8", 'awaited': "", 'eff_after_awaited': "", 'cost': "6 J", 'gain': "2 J"},
    {'card_id': 16, 'name': "Elven magic", 'description': "Your tower gains 10",
     'effects': "y_tower,+10", 'awaited': "", 'eff_after_awaited': "", 'cost': "8 R", 'gain': "2 P"},
    {'card_id': 17, 'name': "Glitter", 'description': "You gain 7 rubies",
     'effects': "y_rubies,+7", 'awaited': "", 'eff_after_awaited': "", 'cost': "5 P", 'gain': "2 J"},
    {'card_id': 18, 'name': "Ogre", 'description': "Deal 5 damage to your opponent",
     'effects': "o_wall,-5", 'awaited': "", 'eff_after_awaited': "", 'cost': "5 P", 'gain': "1 J"},
    {'card_id': 19, 'name': "Bad air", 'description': "You and your opponent gain one more dungeon",
     'effects': "y_dungeons,+1;o_dungeons,+1", 'awaited': "", 'eff_after_awaited': "", 'cost': "8 R", 'gain': "2 R"},
    {'card_id': 20, 'name': "Imps", 'description': "Deal 7 damage to opponent's tower",
     'effects': "o_tower,-7", 'awaited': "", 'eff_after_awaited': "", 'cost': "8 P", 'gain': "1 J"},
    {'card_id': 21, 'name': "Strategy", 'description': "Play or discard two cards",
     'effects': "", 'awaited': "P2", 'eff_after_awaited': "", 'cost': "5 R", 'gain': "3 P"},
    {'card_id': 22, 'name': "Worker goblins", 'description': "Your wall gains 8",
     'effects': "y_wall,+8", 'awaited': "", 'eff_after_awaited': "", 'cost': "6 P", 'gain': "3 P"},

)


class GameEngine:

    def __init__(self, game_object):
        self.game_object = game_object
        self.error_msg = ""

    def get_chosen_card(self, card_number):
        cards_in_hand = json.loads(self.game_object.y_cards)
        card_id = cards_in_hand[card_number]
        card = list(filter(lambda x: x['card_id'] == card_id, CARDS))[0]
        return card

    def is_action_allowed(self, action):
        # checks if selected action is allowed
        # sets self.error_msg if not
        try:
            action_type = action[0]
            card_number = int(action[1])
            assert(0 <= card_number < 6)
            assert(action_type == 'D' or action_type == 'P')

            if action_type == 'D':
                return True
            elif action_type == 'P':
                if self.game_object.awaited != "":
                    if self.game_object.awaited[0] == "D":
                        self.error_msg = "You have to discard a card!"
                        return False
                card = self.get_chosen_card(card_number)

                can_afford = True
                if card['cost'] != "":
                    cost = card['cost'].split(' ')
                    res = cost[1]
                    val = int(cost[0])
                    if res == "J":
                        if self.game_object.y_javas < val:
                            can_afford = False
                    elif res == "R":
                        if self.game_object.y_rubies < val:
                            can_afford = False
                    elif res == "P":
                        if self.game_object.y_pythons < val:
                            can_afford = False

                if not can_afford:
                    self.error_msg = "You can't afford that card, you need " + card['cost']
                    return False
                else:
                    return True

        except:
            return False

    def replace_card(self, card_number):
        cards_in_hand = json.loads(self.game_object.y_cards)
        new_card_id = choice(CARDS)['card_id']
        cards_in_hand[card_number] = new_card_id
        self.game_object.y_cards = json.dumps(cards_in_hand)


    def resolve_action(self, action):
        # modifies self.game_object and returns message

        message = ""

        if self.game_object.awaited != "":
            if self.game_object.awaited[1] == "1":
                self.game_object.awaited = ""
            else:
                val = int(self.game_object.awaited[1])
                letter = self.game_object.awaited[0]
                self.game_object.awaited = letter + str(val - 1)

        action_type = action[0]
        card_number = int(action[1])
        card = self.get_chosen_card(card_number)

        if action_type == "D":
            gain = card['gain'].split(" ")
            res = gain[1]
            change = int(gain[0])
            if res == "J":
                self.game_object.y_javas += change
            elif res == "R":
                self.game_object.y_rubies += change
            elif res == "P":
                self.game_object.y_pythons += change

            message = "You discarded " + card['name'] + " for " + card['gain']
            self.replace_card(card_number)

        elif action_type == "P":

            if card['cost'] != "":
                cost = card['cost'].split(' ')
                res = cost[1]
                val = int(cost[0])
                if res == "J":
                    self.game_object.y_javas -= val
                elif res == "R":
                    self.game_object.y_rubies -= val
                elif res == "P":
                    self.game_object.y_pythons -= val

            if card['effects'] != "":
                effects = card['effects'].split(";")
                for instr in effects:
                    self.game_object.change_val(instr)

            if self.game_object.y_wall < 0:
                self.game_object.y_tower += self.game_object.y_wall
            if self.game_object.o_wall < 0:
                self.game_object.o_tower += self.game_object.o_wall

            if card['awaited'] != "":
                self.game_object.awaited = card['awaited']

            message = "You played " + card['name'] + " with this effects: " + card['description']
            self.replace_card(card_number)

        self.game_object.save()
        self.game_object.correct_vals()

        return message

    def status(self):
        # return winner, status
        # winner: 0 - player, 1 - opponent, -1 - no winner
        # status: 0 - finished, 1 - ongoing

        if self.game_object.y_tower > 99 or self.game_object.o_tower < 1:
            return 0, 0
        elif self.game_object.y_tower < 1 or self.game_object.o_tower > 99:
            return 1, 0

        return -1, 1

    def opponent_affords(self, card):
        can_afford = True
        if card['cost'] != "":
            cost = card['cost'].split(' ')
            res = cost[1]
            val = int(cost[0])
            if res == "J":
                if self.game_object.o_javas < val:
                    can_afford = False
            elif res == "R":
                if self.game_object.o_rubies < val:
                    can_afford = False
            elif res == "P":
                if self.game_object.o_pythons < val:
                    can_afford = False

        return can_afford

    def increases_generators(self, card):
        if card['effects'][:10] == 'y_coffee,+':
            return True
        elif card['effects'][:9] == 'y_mines,+':
            return True
        elif card['effects'][:12] == 'y_dungeons,+':
            return True
        else:
            return False

    def AI_action(self):
        # pretends to choose card and action
        # modifies self.game_object and returns message

        message = ""

        # here will be process of choosing action type and card (involving checking costs)

        card_chosen = False

        # look for card increasing resources generator

        card = CARDS[0]
        action_type = "D"

        for i in range(6):
            candidate = choice(CARDS)
            if self.increases_generators(candidate) and self.opponent_affords(candidate):
                card_chosen = True
                card = candidate
                action_type = "P"
                break

        if card_chosen == False:
            for i in range(6):
                candidate = choice(CARDS)
                if self.opponent_affords(candidate) and candidate['awaited'] == "":
                    card_chosen = True
                    card = candidate
                    action_type = "P"
                    break

        if card_chosen == False:
            card = choice(CARDS)
            action_type = "D"


        # resolving opponent's action

        if action_type == "D":
            gain = card['gain'].split(" ")
            res = gain[1]
            change = int(gain[0])
            if res == "J":
                self.game_object.o_javas += change
            elif res == "R":
                self.game_object.o_rubies += change
            elif res == "P":
                self.game_object.o_pythons += change

            message = "Opponent discarded " + card['name'] + " for " + card['gain']

        elif action_type == "P":

            if card['cost'] != "":
                cost = card['cost'].split(' ')
                res = cost[1]
                val = int(cost[0])
                if res == "J":
                    self.game_object.o_javas -= val
                elif res == "R":
                    self.game_object.o_rubies -= val
                elif res == "P":
                    self.game_object.o_pythons -= val

            # invert o_ with y_
            effects = card['effects'].split(";")
            if len(effects) > 0:
                for instr in effects:
                    inv_instr = ""
                    if instr[0] == "o":
                        inv_instr = "y" + instr[1:]
                    elif instr[0] == "y":
                        inv_instr = "o" + instr[1:]
                    self.game_object.change_val(inv_instr)

            if self.game_object.y_wall < 0:
                self.game_object.y_tower += self.game_object.y_wall
            if self.game_object.o_wall < 0:
                self.game_object.o_tower += self.game_object.o_wall

            message = "Opponent played " + card['name'] + " with this effects: " + card['description']

        self.game_object.save()
        self.game_object.correct_vals()
        return message

    def determine_bars(self):

        def calc(val):
            return max(20, int(1.6*val))

        bars = {'yt': calc(self.game_object.y_tower), 'ot': calc(self.game_object.o_tower),
                'yw': calc(self.game_object.y_wall), 'ow': calc(self.game_object.o_wall)}
        return bars

    def get_cards_data(self):
        cards_data = []
        for i in range(6):
            card = self.get_chosen_card(i).copy()
            card['id'] = i

            # this might need repackaging
            cards_data.append(card)
        return cards_data

    def gain_resources(self):
        self.game_object.y_javas += self.game_object.y_coffee
        self.game_object.o_javas += self.game_object.o_coffee

        self.game_object.y_rubies += self.game_object.y_mines
        self.game_object.o_rubies += self.game_object.o_mines

        self.game_object.y_pythons += self.game_object.y_dungeons
        self.game_object.o_pythons += self.game_object.o_dungeons

        self.game_object.save()
