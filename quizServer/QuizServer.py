#!/usr/bin/env python3

import asyncio
import bottle
import contextlib
import itertools
import sqlite3
import sys
import termios
import time
import tty


@bottle.route('/quiz')
def returnQuiz(limit=100, filename='quiz.sqlite3'):
    conn = sqlite3.connect(filename)
    conn.row_factory = sqlite3.Row  # Allow dict access for each row
    cur = conn.cursor()
    cur.execute('''
        SELECT name, dict, isWord, cardbox, MAX(timestamp)
        AS name, dict, isWord, cardbox, timestamp
        FROM questions
        GROUP BY name
        ORDER BY MAX(timestamp) +  65536 * cardbox*cardbox
        LIMIT ''' + '%d;' % limit)
    print([dict(item) for item in cur])
    conn.close()



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



if __name__ == '__main__':
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    else:
        limit = 100
    print(returnQuiz(limit))
