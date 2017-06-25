#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
import gevent

import bottle
import contextlib
import itertools
import sqlite3
import sys
import time
import tty


class quizServer(bottle.Bottle):
    def __init__(self, sqlfile, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.conn = sqlite3.connect(sqlfile)
        self.conn.row_factory = sqlite3.Row  # Allow dict access for each row
        self.get('/quiz', callback=self.returnQuiz)

    def __del__(self):
        self.conn.close()

    def returnQuiz(self, limit=1000, filename='quiz.sqlite3'):
        cur = self.conn.cursor()
        cur.execute('''
            SELECT name, dict, isWord, cardbox, MAX(timestamp) AS timestamp
            FROM questions
            GROUP BY name
            ORDER BY timestamp +  65536 * cardbox*cardbox
            LIMIT ''' + '%d;' % limit)
        return {'quiz': [dict(item) for item in cur]}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    else:
        limit = 10
    quiz = quizServer('quiz.sqlite3')
    quiz.run(host='0.0.0.0', port=80, server='gevent')
