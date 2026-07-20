
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def load_dictionary():
    '''Load a dictionary from a file and return it as a list of strings'''
    dictionary = []
    return dictionary

def choose_pangram(dictionary):
    '''Pick a base pangram from the dictionary and return it'''
    pangram = ''
    return pangram

def extract_letters(pangram):
    '''Return a list of seven lower case letters based on the chosen pangram'''
    letters = ''
    return letters

def get_word_list(letters, dictionary):
    '''Return a full list of allowed words based on the letters'''
    word_list = []
    return word_list

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
    word_list = get_word_list(letters)
    return {'letters':letters, 'word_list':word_list}

dictionary = load_dictionary()
