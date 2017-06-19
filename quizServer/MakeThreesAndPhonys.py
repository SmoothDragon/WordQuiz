#!/usr/bin/python3

import random
import sqlite3
import time

VOWELS = 'AEIOU'

def twoLetterWords(filename='/usr/local/share/dict/OWL14.txt'):
    '''Extract all two letter words
    '''
    with open(filename, 'rt') as infile:
        for word in infile:
            if len(word) == 3:  # length + \n
                yield word[:-1]  # lose linefeed

def threeLetterWords(filename='/usr/local/share/dict/OWL14.txt'):
    '''Extract all three letter words
    '''
    with open(filename, 'rt') as infile:
        for word in infile:
            if len(word) == 4:  # length + \n
                yield word[:-1]  # lose linefeed

def substituteVowels(word):
    '''Substitute all vowels positions with all vowels
    >>> list(substituteVowels('CAR'))
    ['CAR', 'CER', 'CIR', 'COR', 'CUR']
    >>> list(substituteVowels('ACE'))
    ['ACE', 'ECE', 'ICE', 'OCE', 'UCE', 'ACA', 'ACE', 'ACI', 'ACO', 'ACU']
    '''
    for i in range(len(word)):
        if word[i] in VOWELS:
            yield from (word[:i]+v+word[i+1:] for v in VOWELS)

def buildSQLiteFomWordDict(wordDict, filename='quiz.sqlite3'):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS questions(
                     name       VARCHAR(15) NOT NULL
                     ,dict      VARCHAR(255)
                     ,isWord    INTEGER
                     ,cardbox   INTEGER
                     ,timestamp FLOAT
                     );
                     ''')
    for word in wordDict:
        cur.execute('INSERT INTO questions VALUES(?,?,?,?,?);',
                     (word, 'OWL14', int(wordDict[word]), 0, time.time()))
    conn.commit()

def isPlausible(word):
    '''Word has a *chance* of being real.
    '''
    if len(word) <= 3:
        if word.count('I') > 1:  # No 3 letter word has two Is
            return False
        if word.count('U') > 1:  # Only ULU has two Us
            return False
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    W3 = list(threeLetterWords())
    # Make plausible words via vowel substitution
    P3 = {w:False for word in W3 for w in substituteVowels(word) if isPlausible(w)}
    # Pluralize all two letter words to make plausible 3s
    for word in twoLetterWords():
        P3[word+'S'] = False
    # Add all Collins 3s
    C3 = list(threeLetterWords('/usr/local/share/dict/CSW15.txt'))
    for word in C3:
        P3[word] = False
    # Validate all real words
    for word in W3:
        P3[word] = True
    # Put word list in SQLite3 database
    # P3 = {k:P3[k] for k in random.sample(list(P3), 10)}  # Random subset for testing
    buildSQLiteFomWordDict(P3)
