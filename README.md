# ssh-wise

Lightweight SSH client wrapper around [paramiko](https://www.paramiko.org/) with coloured logging via [log-wise](https://github.com/klaus-moser/log-wise).

## Installation

```bash
pip install git+https://github.com/klaus-moser/ssh-wise.git
```

## Quick start

```python
from ssh_wise import SSH

ssh = SSH()
ssh.connect_(hostname_="192.168.1.1", username_="admin", password_="secret")

stdout, stderr = ssh.exec_command_("pwd")
print(stdout)

ssh.disconnect_()
```

## Key-based authentication

```python
from pathlib import Path
from ssh_wise import SSH

ssh = SSH()
ssh.connect_(
    hostname_="192.168.1.1",
    username_="admin",
    key_filename_=Path("~/.ssh/id_rsa"),
)
```
