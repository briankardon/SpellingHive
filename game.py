from words import dictionary, generate_game_info, ALPHABET
from functools import wraps

test_pangram = 'spelling'
test_words = ['line', 'sign', 'less', 'sell', 'single', 'else', 'seen', 'engine', 'lines', 'sense', 'selling', 'gene', 'signs', 'singles', 'sleep', 'nine', 'seeing', 'engines', 'lens', 'legs', 'penis', 'lies', 'pipe', 'pipeline', 'pine', 'pills', 'slip', 'nipples', 'pill', 'spin', 'illness', 'ieee', 'genes', 'lenses', 'pissing', 'sleeping', 'neil', 'sing', 'eggs', 'espn', 'singing', 'sees', 'piss', 'isle', 'penn', 'peeing', 'glen', 'lips', 'inns', 'signing', 'sells', 'spell', 'genesis', 'inline', 'pins', 'glenn', 'ellis', 'nipple', 'ellen', 'spelling', 'leslie', 'ping', 'issn', 'pipes', 'pens', 'spies', 'sleeps', 'spine']

class WordError(Exception):
    """Exception raised when a word is not valid."""
    pass
class PlayerError(Exception):
    """Exception raised when a problem with a player is found"""
    pass

def check_id_exists(func):
    @wraps(func)
    def inner(game, id, *args, **kwargs):
        if id not in game.players:
            raise PlayerError('Player {id} not found!'.format(id=id))
        return func(game, id, *args, **kwargs)
    return inner

def check_id_available(func):
    @wraps(func)
    def inner(game, id, *args, **kwargs):
        if id in game.players:
            raise PlayerError('Player {id} already exists!'.format(id=id))
        return func(game, id, *args, **kwargs)
    return inner

class Game:
    def __init__(self, letters=None, words=None):
        self.players = {}
        self.played_words = []
        self.started = False
        self.finished = False
        self.letters = None
        self.words = None
        self.reset(letters=letters, words=words)

    def print(self):
        print('SpellingHive game:')
        print('Letters:', self.letters)
        print('Words:', self.words)
        print('Played:', self.played_words)
        print('Started:', self.started)
        print('Finished:', self.finished)
        print('Players:', len(self.players))
        for k, id in enumerate(self.players.keys()):
            player = self.players[id]
            print('Player {k}:'.format(k=k))
            print('   Name:   ', player['name'])
            print('     ID:   ', id)
            print('  score:   ', player['score'])
            print('  words:   ', player['played_words'])

    def reset(self, letters=None, words=None, remove_players=False):
        self.played_words = []
        self.finished = False
        self.started = False

        if remove_players:
            # Delete all players
            self.players = {}
        else:
            # Don't delete players, just clear game info
            for id in self.players:
                self.players[id]['score'] = 0
                self.players[id]['played_words'] = []

        if letters is None or words is None:
            # self.game_info = generate_game_info(dictionary)
            game_info = {'letters':'speling', 'words':test_words}
            self.letters = sorted(game_info['letters'])
            self.words = game_info['words']
        else:
            self.letters = letters
            self.words = words

    @check_id_available
    def add_player(self, id, name, score=0, played_words=None):
        if played_words is None:
            played_words = []

        self.players[id] = dict(
            name=name,
            score=score,
            played_words=played_words
        )

    @check_id_exists
    def get_player_info(self, id):
        return self.players[id]

    @check_id_exists
    def rename_player(self, id, new_name):
        self.players[id]['name'] = new_name

    @check_id_exists
    def get_player_name(self, id):
        return self.players[id]['name']

    @check_id_exists
    def remove_player(self, id):
        del self.players[id]

    @check_id_exists
    def play_word(self, id, word):
        message = ''
        score = 0
        if not self.started:
            message = "Game not started yet!"
        elif not self.finished:
            try:
                self.validate_word(word)
                score = self.get_word_score(word)
                self.players[id]['score'] += score
                self.players[id]['played_words'].append(word)
                self.played_words.append(word)
                if all([w in self.played_words for w in self.words]):
                    # Game over
                    self.finished = True
                    self.started = False
                    message = 'Game over'
                else:
                    message = 'Word accepted'
            except WordError as e:
                message = str(e)
        else:
            message = 'Game already over!'
        return score, message

    def get_winner(self):
        best_score = -1
        winner_ids = []
        for id in self.players:
            score = self.players[id]['score']
            if score > best_score:
                winner_ids = [id]
                best_score = score
            elif score == best_score:
                winner_ids.append(id)
        return winner_ids

    def validate_word(self, word):
        word = word.lower()
        if len(word) < 4:
            raise WordError('Word ("{w}") is "{n}" characters long, but must be at least 4 characters'.format(w=word, n=len(word)))
        if not all([L in ALPHABET for L in word]):
            raise WordError('Word ("{w}") must only contain valid letters'.format(w=word))
        if not all([L in self.letters for L in word]):
            raise WordError('Word ("{w}") must only use allowed letters ({L})'.format(w=word, L=self.letters))
        if word in self.played_words:
            raise WordError('Word ("{w}") already found'.format(w=word))

    def is_pangram(self, word):
        return set(word) == set(self.letters)

    def get_word_score(self, word):
        if len(word) == 4:
            score = 1
        else:
            score = len(word)

        if self.is_pangram(word):
            score += 7

        return score


if __name__ == '__main__':
    print('testing game.py:')
    g = Game()
    g.add_player('player1', 'dude')
    g.add_player('player2', 'other dude')
    word = 'spelling'
    score, msg = g.play_word('player1', word)
    print('Played', word, 'for', score, 'response', msg)
    word = 'spell'
    score, msg = g.play_word('player2', word)
    print('Played', word, 'for', score, 'response', msg)
    word = 'pipe'
    score, msg = g.play_word('player1', word)
    print('Played', word, 'for', score, 'response', msg)
    word = 'nipple'
    score, msg = g.play_word('player2', word)
    print('Played', word, 'for', score, 'response', msg)
    word = 'spell'
    score, msg = g.play_word('player1', word)
    print('Played', word, 'for', score, 'response', msg)
    word = 'fantastic'
    score, msg = g.play_word('player1', word)
    print('Played', word, 'for', score, 'response', msg)
    g.print()
