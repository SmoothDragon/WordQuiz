#!/usr/bin/env python3

import unittest
from kleinbottle import KleinBottle

class TestMethod(unittest.TestCase):
    def test_parseURL(self):
        self.assertEqual(
            KleinBottle.parseURL('/one/two/three?a=1&b=2&b=3'),
            (['one', 'two', 'three'], {'b': ['2', '3'], 'a': ['1']})
                        )

if __name__ == '__main__':
    unittest.main()
