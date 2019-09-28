import json
from random import choice

# placeholder cards for testing
# awaited can have single action/number pair
# cost and discard can affect only one resource type
CARDS = (
    {'card_id': 0, 'name': "A", 'description': "aaaa", 'effects': "o_wall,-5", 'awaited': "", 'eff_after_awaited': "", 'cost': "3 P", 'discard': "2 P"},
    {'card_id': 1, 'name': "B", 'description': "bbbb", 'effects': "y_wall,+5", 'awaited': "", 'eff_after_awaited': "", 'cost': "3 J", 'discard': "1 J"},
    {'card_id': 2, 'name': "C", 'description': "cccc", 'effects': "", 'awaited': "D2", 'eff_after_awaited': "", 'cost': "5 R", 'discard': "1 J"},
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

            effects = card['effects'].split(";")
            for instr in effects:
                self.game_object.change_val(instr)
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

    def AI_action(self):
        # pretends to choose card and action
        # modifies self.game_object and returns message

        message = ""

        # here will be process of choosing action type and card (involving checking costs)

        #

        card = list(filter(lambda x: x['card_id'] == 0, CARDS))[0]
        action_type = "P"

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
            for instr in effects:
                inv_instr = ""
                if instr[0] == "o":
                    inv_instr = "y" + instr[1:]
                elif instr[0] == "y":
                    inv_instr = "o" + instr[1:]
                self.game_object.change_val(inv_instr)

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
            card = self.get_chosen_card(i)

            # this might need repackaging
            cards_data.append(card)
        return cards_data

