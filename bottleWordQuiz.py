#!/usr/bin/env python

from bottle import route, run


@route('/json')
def basicJSON():
    return {
        'quizOrder': ['CAT', 'DOG', 'BIZ', 'FUZ', 'WHZ', 'ZUZ'],
        'wordValid': {
            'CAT': True,
            'BIZ': True,
            'FUZ': False,
            'WHZ': False,
            'ZUZ': True,
            'DOG': True,
            },
        }


run(host='localhost', port=9000, debug=True)
