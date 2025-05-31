#!/usr/bin/env python3

# Filename: main.py

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


""" SSH Class"""

import paramiko

from pathlib import Path
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException

__author__ = "tg4nd4lf"
__version__ = "1.2"


class SSH:
    """
    # Example
    import os
    from dotenv import load_dotenv
    load_dotenv('../.env')  # Load the environment variables from the .env file

    ssh_client_ = SSH()

    ssh_client_.connect_(hostname_=os.getenv('HOSTNAME'),
                         username_=os.getenv('USERNAME'),
                         password_=os.getenv('PASSWORD'))

    response_ = ssh_client_.exec_command_('pwd')
    print(response_)

    ssh_client_.disconnect_()
    """

    def __init__(self):
        self.client_ = paramiko.SSHClient()
        self.client_.load_system_host_keys()
        self.client_.set_missing_host_key_policy(paramiko.WarningPolicy)

    def __repr__(self):
        return f'SSH: {self.client_}'

    def connect_(self, hostname_: str, username_: str, password_: str = None,
                 key_filename_: Path = None, port_: int = 22, timeout_: int = 30) -> 'SSH':
        """
        Connect.

        :param hostname_: Hostname/IP of device.
        :param username_: Username.
        :param password_: String.
        :param key_filename_: Keyfile.
        :param port_: Port of device. Default: 22.
        :param timeout_: Connection timeout in seconds. Default: 30 seconds.
        :return:
        """

        print("Connect to client...")

        try:
            self.client_.connect(
                hostname=hostname_,
                username=username_,
                password=password_,
                key_filename=key_filename_,
                port=port_,
                timeout=timeout_
            )

            print("Connected to client!")
            return self

        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials.")

        except paramiko.BadHostKeyException as err:
            print("Unable to verify server's host key:", err)

        except paramiko.SSHException as err:
            print("Unable to establish SSH connection:", err)

        except Exception as err:
            print("General error occurred:", err)

    def exec_command_(self, command_: str) -> tuple[list[str], list[str]]:
        """
        Execute a command on the SSH client and return stdout and stderr.

        :param command_: Command to be executed as a string.
        :return: A tuple containing stdout lines and stderr lines.
        """
        try:
            # Execute the command
            _, stdout, stderr = self.client_.exec_command(command=command_)

            # Wait for the command to complete
            exit_status = stdout.channel.recv_exit_status()

            # Read stdout and stderr
            stdout_lines = stdout.read().decode('utf-8', errors='replace').splitlines()
            stderr_lines = stderr.read().decode('utf-8', errors='replace').splitlines()

            if exit_status != 0:
                print(f"Command '{command_}' exited with status {exit_status}")

            return stdout_lines, stderr_lines

        except TimeoutError as err:
            print(f"Unable to execute command due to timeout: {err}")
            return [], [str(err)]

        except SSHException as err:
            print(f"Unable to execute command due to SSH error: {err}")
            return [], [str(err)]

    def disconnect_(self) -> bool:
        """
        Disconnect from device.

        :return: True: Success. False: Failure.
        """

        try:
            self.client_.close()
            print("Connection closed.")
            return True

        except SSHException as err:
            print("Unable to close connection: %s" % err)
            return False


if __name__ == "__main__":
    pass
