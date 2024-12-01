import unittest

import click
from click.testing import CliRunner


@click.command()
def hello():
    click.echo("Hello, World!")


class TestClick(unittest.TestCase):
    def test_hello(self):
        runner = CliRunner()
        result = runner.invoke(hello)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Hello, World!", result.output)


if __name__ == "__main__":
    unittest.main()
