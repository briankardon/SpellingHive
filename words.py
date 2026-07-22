from copy import copy
from random import choice
with open('/Users/silaskardon/Documents/english3.txt') as file:
    text=file.readlines()
    letter7=copy(text)
    for word in text:
        if len(word)<7:
            letter7.remove(word)
    fail=[]
    for maybe in letter7:
        letters=[]
        for letter in list(maybe):
            if letter in letters:
                fail.append(maybe)
                break
            letters.append(letter)
    for failing in fail:
        letter7.remove(failing)
    letter7 = [item.strip() for item in letter7]
    print('checking correct pangram...')
    while True:
        spellwords=[]
        breaker=False
        pangram=choice(letter7)
        good=False
        for words in text:
            for letter in words:
                goodword=True
                if not letter in list(pangram):
                    goodword=False
                    break
            if goodword==True:
                spellwords.append(words)
                breaker=True
        if len(spellwords)>0:
            breaker=True
        else:
            print('oh,no!!!')
        if breaker:
            break
print(pangram)
print(spellwords)
