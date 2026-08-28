#!/usr/bin/env python3

# Filename: ssh.py

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""SSH client wrapper around paramiko."""

from __future__ import annotations

import paramiko
from log_wise import get_logger
from pathlib import Path
from paramiko.ssh_exception import SSHException

__author__ = "tg4nd4lf"
__version__ = "2.0.0"

log = get_logger(__name__)


class SSH:
    """Lightweight SSH client with automatic host-key handling and logging.

    Example
    -------
    >>> from ssh_wise import SSH
    >>> ssh = SSH()
    >>> ssh.connect_(hostname_="192.168.1.1", username_="admin", password_="secret")
    >>> stdout, stderr = ssh.exec_command_("pwd")
    >>> ssh.disconnect_()
    """

    def __init__(self) -> None:
        self.client_ = paramiko.SSHClient()
        self.client_.load_system_host_keys()
        self.client_.set_missing_host_key_policy(paramiko.WarningPolicy)

    def __repr__(self) -> str:
        return f"SSH: {self.client_}"

    def connect_(
        self,
        hostname_: str,
        username_: str,
        password_: str | None = None,
        key_filename_: Path | None = None,
        port_: int = 22,
        timeout_: int = 30,
    ) -> SSH | None:
        """Connect to a remote host.

        Parameters
        ----------
        hostname_:
            Hostname or IP address of the device.
        username_:
            SSH username.
        password_:
            SSH password (optional when using key-based auth).
        key_filename_:
            Path to a private key file.
        port_:
            SSH port (default 22).
        timeout_:
            Connection timeout in seconds (default 30).

        Returns
        -------
        SSH | None
            ``self`` on success, ``None`` on failure.
        """
        log.info("Connecting to %s:%d …", hostname_, port_)

        try:
            self.client_.connect(
                hostname=hostname_,
                username=username_,
                password=password_,
                key_filename=key_filename_,
                port=port_,
                timeout=timeout_,
            )
            log.info("Connected to %s:%d", hostname_, port_)
            return self

        except paramiko.AuthenticationException:
            log.error("Authentication failed — verify your credentials.")

        except paramiko.BadHostKeyException as err:
            log.error("Unable to verify server's host key: %s", err)

        except paramiko.SSHException as err:
            log.error("Unable to establish SSH connection: %s", err)

        except Exception as err:
            log.error("General error occurred: %s", err)

        return None

    def exec_command_(self, command_: str) -> tuple[list[str], list[str]]:
        """Execute a command on the remote host.

        Parameters
        ----------
        command_:
            Shell command to execute.

        Returns
        -------
        tuple[list[str], list[str]]
            ``(stdout_lines, stderr_lines)``
        """
        try:
            _, stdout, stderr = self.client_.exec_command(command=command_)
            exit_status = stdout.channel.recv_exit_status()

            stdout_lines = stdout.read().decode("utf-8", errors="replace").splitlines()
            stderr_lines = stderr.read().decode("utf-8", errors="replace").splitlines()

            if exit_status != 0:
                log.warning(
                    "Command '%s' exited with status %d", command_, exit_status
                )

            return stdout_lines, stderr_lines

        except TimeoutError as err:
            log.error("Command timed out: %s", err)
            return [], [str(err)]

        except SSHException as err:
            log.error("SSH error during command execution: %s", err)
            return [], [str(err)]

    def disconnect_(self) -> bool:
        """Close the SSH connection.

        Returns
        -------
        bool
            ``True`` on success, ``False`` on failure.
        """
        try:
            self.client_.close()
            log.info("Connection closed.")
            return True

        except SSHException as err:
            log.error("Unable to close connection: %s", err)
            return False
