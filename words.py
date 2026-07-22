
from copy import copy
from random import choice
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
VOWELS = 'aeiou'

def load_dictionary():
    '''Load a dictionary from a file and return it as a list of strings'''
    with open('english3.txt') as file:
        text=file.readlines()
    dictionary = [part.strip() for part in text]
    return dictionary
def choose_pangram(dictionary):
    '''Pick a base pangram from the dictionary and return it'''
    letter7=[word for word in dictionary if 7<len(word)<10 and len(set(word))==7]
    print('checking correct pangram...')
    return choice(letter7)
def choose_panagram(dictionary):
    return choose_pangram(dictionary)
def extract_letters(pangram):
    '''Return a list of seven lower case letters based on the chosen pangram'''
    theletters=list(set(pangram))
    letters = theletters
    return letters

def get_word_list(pangram, dictionary):
    '''Return a full list of allowed words based on the letters'''
    while True:
        spellwords=[]
        breaker=False
        good=False
        for words in dictionary:
            for letter in words:
                goodword=True
                if not letter in list(pangram):
                    goodword=False
                    break
            if goodword==True and len(words)>3:
                spellwords.append(words)
                breaker=True
        if len(spellwords)>0:
            breaker=True
        else:
            print('oh,no!!!')
        if breaker:
            break
    return spellwords

def validate_letters(letters):
    # Check that these are 7 valid letters
    letters = letters.lower()
    if len(letters) != 7:
        raise ValueError(
            'letters must have 7 letters, instead got ' + letters
        )
    if len(letters) != len(set(letters)):
        raise ValueError(
            'letters argument must be 7 unique letters, instead got '+letters
        )
    if not all([L in ALPHABET for L in letters]):
        raise ValueError(
            'letters must all be lowercase letters, instead got '+letters
        )
    return letters

def generate_game_info(dictionary):
    '''Shortcut that invokes all the functions in order'''
    pangram = choose_pangram(dictionary)
    letters = extract_letters(pangram)
    word_list = get_word_list(pangram,dictionary)
    return {'letters':letters, 'word_list':word_list}
dictionary = load_dictionary()

if __name__ == '__main__':
    game_info = generate_game_info(dictionary)
    print(game_info)
