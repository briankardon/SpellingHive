from words import dictionary, generate_game_info

class Game:
    def __init__(self):
        self.game_info = generate_game_info(dictionary)
        pass
    
