#!/usr/bin/env python3

from gevent import monkey; monkey.patch_all()
import gevent

import bottle
import contextlib
import itertools
import sqlite3
import sys
import time
import tty
import abc

class QuizDataBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getQuestions(self, limit=None):
        raise NotImplementedError('getQuestions must be instantiated.')


class QuizDataBase_sqlite3(QuizDataBase):
    '''Provides sqecific services:
    getQuestions
    This particular instantiation uses sqlite3
    '''
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row  # Allow dict access for each row

    def getQuestions(self, limit=None):
        query = '''
            SELECT name, dict, isWord, cardbox, MAX(timestamp) AS timestamp
            FROM questions
            GROUP BY name
            ORDER BY timestamp +  65536 * cardbox*cardbox
            '''
        if limit is None:
            postscript = ';'
        else:
            postscript = 'LIMIT %d;' % limit
        cur = self.conn.cursor()
        cur.execute(query + postscript)
        return [dict(item) for item in cur]

    def __del__(self):
        self.conn.close()


class quizServer(bottle.Bottle):
    def __init__(self, quizDB, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.get('/quiz', callback=self.returnQuiz)
        self.DB = quizDB

    def returnQuiz(self, limit=None):
        questions = self.DB.getQuestions(limit=limit)
        return {'quiz': questions}


def main():
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    else:
        limit = 10
    quizDB = QuizDataBase_sqlite3('quiz.sqlite3')
    quiz = quizServer(quizDB)
    quiz.run(host='0.0.0.0', port=80, server='gevent')


if __name__ == '__main__':
    main()
