import unittest

from best403unlocker_py.cli import cli
from click.testing import CliRunner


class TestBest403Unlocker(unittest.TestCase):
    def test_default(self):
        runner = CliRunner()
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "DNS servers have been searched and set successfully.", result.output
        )


if __name__ == "__main__":
    unittest.main()
