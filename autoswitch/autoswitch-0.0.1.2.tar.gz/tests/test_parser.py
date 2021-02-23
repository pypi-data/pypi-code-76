import unittest
from autoswitch import cli


class TestParser(unittest.TestCase):

    def test_serial_list_port(self):

        args = cli.get_args(["serial", "--list-port"])

        self.assertTrue(args["list_port"])

        args = cli.get_args(["serial"])

        self.assertFalse(args["list_port"])

    def test_serial_username(self):

        username = "admin"

        args = cli.get_args(["serial", "--username", username])
        self.assertEqual(args["username"], username)

        args = cli.get_args(["serial", "-l", username])
        self.assertEqual(args["username"], username)

    def test_serial_password(self):

        password = "cisco"

        args = cli.get_args(["serial", "--password", password])
        self.assertEqual(args["password"], password)

        args = cli.get_args(["serial", "-p", password])
        self.assertEqual(args["password"], password)

    def test_serial_secret(self):

        secret = "class"

        args = cli.get_args(["serial", "--secret", secret])
        self.assertEqual(args["secret"], secret)

        args = cli.get_args(["serial", "-s", secret])
        self.assertEqual(args["secret"], secret)

    def test_serial_auth(self):

        username = "admin"
        password = "cisco"
        secret = "class"

        args = cli.get_args(
            ["serial", "--username", username, "--password", password, "--secret", secret])

        self.assertEqual(args["username"], username)
        self.assertEqual(args["password"], password)
        self.assertEqual(args["secret"], secret)

        args = cli.get_args(
            ["serial", "-l", username, "-p", password, "-s", secret])

        self.assertEqual(args["username"], username)
        self.assertEqual(args["password"], password)
        self.assertEqual(args["secret"], secret)


if __name__ == "__main__":
    unittest.main()
