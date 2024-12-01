
import unittest

import requests


class TestRequests(unittest.TestCase):
    def test_get(self):
        response = requests.get('https://httpbin.org/get',timeout=2)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()