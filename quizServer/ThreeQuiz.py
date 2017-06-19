#!/usr/bin/env python3

import asyncio
import contextlib
import itertools
import sqlite3
import sys
import termios
import time
import tty

def getch(echo=True):
    old_settings = termios.tcgetattr(0)
    new_settings = old_settings[:]
    new_settings[3] &= ~termios.ICANON
    if not echo:
        new_settings[3] &= ~termios.ECHO
    try:
        termios.tcsetattr(0, termios.TCSANOW, new_settings)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(0, termios.TCSANOW, old_settings)
    return ch


def getQuestions(conn: 'SQLconnection', limit):
    # find latest timestamp entry for each word
    # order by timestamp + function(cardbox) seconds
    cur = conn.cursor()
    cur.execute('''
        SELECT name, dict, isWord, cardbox, MAX(timestamp) FROM questions
        GROUP BY name
        ORDER BY MAX(timestamp) +  65536 * cardbox*cardbox
        LIMIT ''' + '%d;' % limit)
    yield from cur


def askQuestions(conn, questions):
    for item in questions:
        print(item['name'])
        # Display questions
        # await response
        # correct -> update databse
        # incorrect -> update databse
        print('%s %02d %s' % (item[1], item[3], item[0]))
        ch = getch(echo=False)
        correct = int(ch in 'yY,') == item[2]
        if correct:
            print('Correct')
            cardbox = item[3] + 1
        else:
            print('Wrong')
            cardbox = 0
        update = list(item)
        update[3] = cardbox
        update[4] = time.time()
        cur = conn.cursor()
        cur.execute('INSERT INTO questions VALUES(?,?,?,?,?);', update)
    conn.commit()


@contextlib.contextmanager
def getDBConn(filename='quiz.sqlite3'):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row  # Allow dict access for each row
    yield conn
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    else:
        limit = 100
    # Read in number of questions default (limit)
    # sort according to cardbox and timestamp
    # limit to top 100
    with getDBConn() as conn:
        quiz = getQuestions(conn, limit)
        askQuestions(conn, quiz)

    """
    asyncio.wait_for(keypress)
    for name in questions:
        # print question
        # , yes . no  q quit
        # commit new answers to db
        cur.execute('INSERT INTO questions VALUES(?,?,?,?);',
                     (word, int(wordDict[word]), 0, time.time()))
        pass

    """
