import unittest
from unittest.mock import MagicMock, patch

from paramiko import SSHClient
from paramiko.ssh_exception import SSHException

from ssh_wise import SSH


class SSHTest(unittest.TestCase):

    def test_init_PASS(self):
        ssh_ = SSH()
        self.assertIsInstance(ssh_.client_, SSHClient)

    @patch("ssh_wise.ssh.SSH.connect_", MagicMock(return_value=SSHClient))
    def test_connect_PASS(self):
        ssh_ = SSH()
        ret_ = ssh_.connect_(
            hostname_="1.1.1.1",
            port_=22,
            username_="test",
            password_="test",
        )
        self.assertEqual(ret_, SSHClient)

    @patch("ssh_wise.ssh.SSH.connect_", MagicMock(side_effect=SSHException))
    def test_connect_FAIL(self):
        ssh_ = SSH()
        with self.assertRaises(SSHException):
            ssh_.connect_(
                hostname_="1.1.1.1",
                port_=22,
                username_="test",
                password_="test",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
