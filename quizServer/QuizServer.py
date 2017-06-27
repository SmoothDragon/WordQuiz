#!/usr/bin/env python3

from gevent import monkey; monkey.patch_all()
import gevent

import bottle
import argparse
import contextlib
import itertools
import sqlite3
import sys
import time
import tty
import abc

from kleinBottle import kleinBottle

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

"""

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
"""

def parseArguments():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Start advisor service.')
    parser.add_argument('-p', action='store', default='8880',
                        dest='port', help='Port (default 8880)')
    parser.add_argument('-d', action='store_true', default=False,
                        dest='daemon', help='Run as daemon')
    parser.add_argument('-l', action='store_true', default=False,
                        dest='logger', help='Log service activity')
    parser.add_argument('-f', action='store', dest='logfile',
                        default='/var/log/advisor/advisor.log',
                        help='Logfile name')
    parser.add_argument('-t', action='store_true', default=False,
                        dest='testing', help='Run doctests')
    parser.add_argument('--datafile', action='store', dest='datafile',
                        default='/var/lib/advisor/advisor.sqlite3',
                        help='Data directory')
    return parser.parse_args()

def testCallback(**args):
    quizDB = QuizDataBase_sqlite3('quiz.sqlite3')
    quiz = quizBD.getQuestions()
    return {'quiz': quiz}, 'application/json', 200

def main():
    args = parseArguments()
    example = KleinBottle(testCallback)
    example.run(host='0.0.0.0', port=int(args.port), server='gevent')


if __name__ == '__main__':
    main()
