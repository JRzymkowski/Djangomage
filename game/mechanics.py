cards = []

class GameEngine():

    def __init__(self, game_object):
        self.game_object = game_object
        self.error_msg = ""

    def is_action_allowed(self):
        # checks if selected action is allowed
        pass

    def resolve_action(self, action):
        # modifies self.game_object and returns message
        return ""

    def status(self):
        # return winner, status
        # winner: 0 - player, 1 - opponent, -1 - no winner
        # status: 0 - finished, 1 - ongoing
        # fixes y_tower and o_tower

        return -1, 1

    def AI_action(self):
        # modifies self.game_object and returns message
        return ""

