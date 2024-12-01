
import time
import unittest

from tqdm import tqdm


class TestTQDM(unittest.TestCase):
    def test_tqdm(self):
        for _ in tqdm(range(100)):
            time.sleep(0.01)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()