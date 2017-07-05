#!/usr/bin/env python3

import argparse
import multiprocessing
import requests
import unittest
import boddle

import klein


def testCallback(**args):
    print(args)
    return args, 'application/json', 200

Examples = [
    dict(
         url='http://localhost:8889/one/two/three?b=2&b=3&a=1',
         method='GET',
         json={},
        ),
    ]

# This is more of an integration test
# Move into own function, start service and run live
class TestBottleWebFramework(unittest.TestCase):
    def setUp(self):
        self.framework = klein.BottleWebFramework(testCallback)
        self.proc = multiprocessing.Process(
            target=self.framework.run,
            kwargs=dict(host='localhost', port=8889, quiet=True, ),
            )
        self.proc.start()
        # Loop until connection is up
        while True:
            try:
                data = requests.get('http://localhost:8889')
            except requests.exceptions.ConnectionError:
                continue
            break

    def tearDown(self):
        self.proc.terminate()

    def test_getURL_example(self):
        for example in Examples:
            # result = requests.get(example['url']).json()
            result = requests.get('http://localhost:8889/one/two/three',
                                  params={'a':1, 'b':[2,3]})
            print(result.url)
            self.assertEqual(
                result.json()['url'],
                result.url,
                )

def parseArguments():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Start advisor service.')
    parser.add_argument('-p', action='store', default='8889',
                        dest='port', help='Port (default 8889)')
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

def main():
    args = parseArguments()
    port = int(args.port)
    example = klein.BottleWebFramework(testCallback)
    proc = multiprocessing.Process(
        target=example.run,
        kwargs=dict(host='0.0.0.0', port=port, ),
        )
    proc.start()
    # Loop until connection is up
    while True:
        try:
            data = requests.get('http://localhost:8889')
        except requests.exceptions.ConnectionError:
            continue
        break
    url='http://127.0.0.1/one/two/three?a=1&b=2&b=3',
    data = requests.get('http://localhost:8889', params={'a':1, 'b':[2,3]})
    print(data.json())
    proc.terminate()

if __name__ == '__main__':
    unittest.main()
    # main()
