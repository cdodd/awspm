awspm (AWS Profile Manager)
===========================

A TUI tool for managing AWS key pairs and roles.

```
   _____ _ _ _ _____ _____ _____
  |  _  | | | |   __|  _  |     |
  |     | | | |__   |   __| | | |
  |__|__|_____|_____|__|  |_|_|_|

  Current profile: dev (using temporary credentials)

    1 - Request temporary credentials
    2 - Assume a role
    3 - Set default key pair/assumed role
    4 - Manage key pairs/assumed roles

    5 - Exit
```

This is a python based tool for managing your `~/.aws/credentials` file when you
have multiple AWS key pairs or assumed roles. It provides switching between key
pairs, requesting temporary credentials (for MFA enabled key pairs) and assuming
roles.

Installation
------------

`awspm` is currently targeted at Python 3.6. The instructions below assume you
have `pip` installed.

### Virtualenv on *nix

```bash
$ git clone http://github.com/cdodd/awspm
$ cd awspm
$ virtualenv venv --no-site-packages
$ source venv/bin/activate
$ pip install -r requirements.txt

# Run the Application
$ ./awspm
```

### Manual Global Install on *nix

```bash
$ sudo git clone http://github.com/cdodd/awspm /opt/awspm
$ sudo -H pip install -r /opt/awspm/requirements.txt
$ sudo ln -s /opt/awspm/awspm /usr/local/bin/awspm

# Run the application
$ awspm
```

Usage
-----

You can use the up/down arrows to navigate, and enter/return to make a
selection. You can also use the left/right arrows; left to return to the
previous screen/exit the application, right to make a selection. You can also
use `ctrl` + `c` at any point the exit the application.

You can specify a config file to use with `-c`/`--config` as per the usage
instructions:

```bash
$ awspm -h
usage: awspm [-h] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to config file (defaults to
                        /home/cdodd/.awspm.json)
```

This defaults to `$HOME/.awspm.json` if not specified. You do not need a config
file before running the application. Key pairs and roles you enter will be saved
in the config file.

### Enable 2FA in IAM

You will need to edit your IAM policy to enable 2FA on selected actions and
resources in your account.
Do this by adding a `MultiFactorAuthAge` condition on the actions/resources you want to enforce 2FA on.
For example, (1h age):
```
"Condition":{
    "NumericLessThan": {
        "aws:MultiFactorAuthAge":"3600"
     },
     "Null": {
          "aws:MultiFactorAuthAge": "false"
     }
 }

```

More info on enabling 2FA in IAM can be found in the [AWS documentation](http://docs.aws.amazon.com/IAM/latest/UserGuide/MFAProtectedAPI.html)

### Add a Key Pair

Select `Manage key pairs/assumed roles` > `Add a key pair`, then enter the
required details:

```
awspm > Manage key pairs/assumed roles

  Select an option:

    1 - ┌────────────────────────────────────────┐
    2 - │           Add a Key Pair:              │
    3 - │                                        │
    4 - │    Key pair name:                      │
    5 - │     IAM username:                      │
    6 - │    Access key ID:                      │
    7 - │Secret access key:  (hidden)            │
    8 - │       Account ID:                      │
        │   Default region:                      │
    9 - └────────────────────────────────────────┘
```

### Request Temporary Credentials

Select `Request temporary credentials`. At the next screen select the key pair
to be used, then enter the 6 digit MFA token. Once the temporary credentials
have successfully been requested they will be enabled on the key pair used to
obtain them. They will also then be set as the default profile.

### Add a Role

Select `Manage key pairs/assumed roles` > `Add a role`. Select the key pair
associated the new role, enter a role name, then the role ARN.

### Assume a Role

Select `Assume a role`, then choose the desired role to assume.

### Set Default Key Pair/Assumed Role

Select `Set default key pair/assumed role`, then select the desired key
pair/assumed role you want to use as the default.
