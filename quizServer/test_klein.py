#!/usr/bin/env python3

import unittest
import boddle

from klein import Klein, bottleWebFramework, Request


def testCallback(**args):
    print(args)
    return args, 'application/json', 200

class TestMethod(unittest.TestCase):
    def test_parseURL(self):
        self.assertEqual(
            Klein.parseURL('/one/two/three?a=1&b=2&b=3'),
            (['one', 'two', 'three'], {'b': ['2', '3'], 'a': ['1']})
                        )
class TestKlein(unittest.TestCase):
    def setUp(self):
        self.framework = bottleWebFramework(testCallback)

    def test_getRequestInfo(self):
        params = dict(
                      url='http://127.0.0.1/one/two/three?a=1&b=2&b=3',
                      method='GET',
                      json={},
                     )
        request = Request(**params)
        print(request)
        with boddle.boddle(**params):
            self.assertEqual(self.framework.getRequestInfo(), request)


if __name__ == '__main__':
    unittest.main()
