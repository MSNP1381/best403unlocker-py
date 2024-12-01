import unittest

import dns.resolver


class TestDNSPython(unittest.TestCase):
    def test_resolve(self):
        result = dns.resolver.resolve("example.com", "A")
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()
