#!/usr/bin/env python3

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
         url='http://127.0.0.1/one/two/three?a=1&b=2&b=3',
         method='GET',
         json={},
        ),
    ]

class TestMethod(unittest.TestCase):
    def test_parseURL(self):
        self.assertEqual(
            klein.Klein.parseURL('/one/two/three?a=1&b=2&b=3'),
            (['one', 'two', 'three'], {'b': ['2', '3'], 'a': ['1']})
                        )
class TestMockWebFramework(unittest.TestCase):
    def setUp(self):
        self.example = Examples

    def test_getURL_example(self):
        for example in self.example:
            framework = klein.MockWebFramework(**example)
            self.assertEqual(
                framework.getURL(),
                example['url'],
                )

    def test_getMethod_example(self):
        for example in self.example:
            framework = klein.MockWebFramework(**example)
            self.assertEqual(
                framework.getMethod(),
                example['method'],
                )

    def test_getJSON_example(self):
        for example in self.example:
            framework = klein.MockWebFramework(**example)
            self.assertEqual(
                framework.getJSON(),
                example['json'],
                )

class TestKlein(unittest.TestCase):
    def setUp(self):
        self.framework = klein.BottleWebFramework(testCallback)

    def test_getRequestInfo(self):
        params = dict(
                      url='http://127.0.0.1/one/two/three?a=1&b=2&b=3',
                      method='GET',
                      json={},
                     )
        with boddle.boddle(**params):
            self.assertEqual(self.framework.getURL(), params['url'])

"""
# This is more of an integration test
# Move into own function, start service and run live
class TestBottleWebFramework(unittest.TestCase):
    def setUp(self):
        self.framework = klein.BottleWebFramework(testCallback)
        self.proc = multiprocessing.Process(
            target=self.framework.run,
            kwargs=dict(host='localhost', port=8888, quiet=True, ),
            )
        self.proc.start()
        # Loop until connection is up
        while True:
            try:
                data = requests.get('http://localhost:8888')
            except requests.exceptions.ConnectionError:
                continue
            break

    def tearDown(self):
        self.proc.terminate()

    def test_getURL_example(self):
        for example in Examples:
            result = requests.get(example['url']).json()
            self.assertEqual(
                result['url'],
                example['url'],
                )

"""

if __name__ == '__main__':
    unittest.main()
