# Python standard library modules
import configparser
import curses
import json
import os
import sys


class ConfigError(Exception):
    pass


class Config(object):
    def __init__(self, config_path):
        self.config_path = config_path
        if os.path.isfile(config_path):
            try:
                config_raw = open(config_path, 'r').read()
            except IOError:
                raise ConfigError('Could not open/read config file "{0:s}"'.format(config_path))

            try:
                self.data = json.loads(config_raw)
            except ValueError:
                raise ConfigError('Could not parse config file "{0:s}" as JSON'.format(config_path))
        else:
            self.data = {
                'assumed_roles': {},
                'default_profile_name': None,
                'default_profile_type': None,
                'key_pairs': {},
            }

    def get_active_key_pair(self, key_pair_name):
        if key_pair_name not in self.data['key_pairs']:
            raise ConfigError('"{0:s}" key pair not found in config'.format(key_pair_name))

        if self.data['key_pairs'][key_pair_name]['use_temporary_credentials']:
            key_data = {
                'aws_access_key_id': self.data['key_pairs'][key_pair_name]['temporary_credentials']['access_key_id'],
                'aws_secret_access_key': self.data['key_pairs'][key_pair_name]['temporary_credentials']['secret_access_key'],
                'aws_session_token': self.data['key_pairs'][key_pair_name]['temporary_credentials']['session_token'],

                # aws_security_token is deprecated, but required by boto
                'aws_security_token': self.data['key_pairs'][key_pair_name]['temporary_credentials']['session_token'],
            }
        else:
            key_data = {
                'aws_access_key_id': self.data['key_pairs'][key_pair_name]['access_key_id'],
                'aws_secret_access_key': self.data['key_pairs'][key_pair_name]['secret_access_key'],
            }

        for k, v in self.data['key_pairs'][key_pair_name]['options'].items():
            key_data[k] = v

        return key_data

    def save(self):
        # Check the config has at least one keypair before attempting to save it
        if len(self.data['key_pairs'].keys()) == 0:
            raise ConfigError('No keypairs in config')

        # Write the config file data
        try:
            open(self.config_path, 'w').write(json.dumps(self.data, sort_keys=True, indent=2, separators=(',', ': ')))
        except IOError:
            raise ConfigError('Could not open the config file "{0:s}" for writing'.format(self.config_path))

        # Create the AWS credentials INI file
        config_data = configparser.ConfigParser()
        default_profile_name = self.data['default_profile_name']
        if self.data['default_profile_type'] == 'assumed_role':
            config_data['default'] = {
                'aws_access_key_id': self.data['assumed_roles'][default_profile_name]['access_key_id'],
                'aws_secret_access_key': self.data['assumed_roles'][default_profile_name]['secret_access_key'],
                'aws_session_token': self.data['assumed_roles'][default_profile_name]['session_token'],

                # aws_security_token is deprecated, but required by boto
                'aws_security_token': self.data['assumed_roles'][default_profile_name]['session_token'],
            }
            options = self.data['assumed_roles'][default_profile_name].get('options', {})
            for k, v in options.items():
                config_data['default'][k] = v
        else:
            config_data['default'] = self.get_active_key_pair(default_profile_name)

        # Output the rest of the key pairs & assumed roles
        for key_pair_name in self.data['key_pairs'].keys():
            config_data[key_pair_name] = self.get_active_key_pair(key_pair_name)

        for role_name in self.data['assumed_roles'].keys():
            config_data[role_name] = {
                'aws_access_key_id': self.data['assumed_roles'][role_name]['access_key_id'],
                'aws_secret_access_key': self.data['assumed_roles'][role_name]['secret_access_key'],
                'aws_session_token': self.data['assumed_roles'][role_name]['session_token'],

                # aws_security_token is deprecated, but required by boto
                'aws_security_token': self.data['assumed_roles'][role_name]['session_token'],
            }
            options = self.data['assumed_roles'][role_name].get('options', {})
            for k, v in options.items():
                config_data[role_name][k] = v

        # Create ~/.aws directory if it doesn't already exist
        aws_config_dir = os.path.join(os.path.expanduser('~'), '.aws')
        os.makedirs(aws_config_dir, exist_ok=True)

        # Write the AWS credentials INI file
        aws_config_file = os.path.join(aws_config_dir, 'credentials')
        try:
            with open(aws_config_file, 'w') as configfile:
                config_data.write(configfile)
        except IOError:
            raise ConfigError('Could not write the AWS credentials file "{0:s}"'.format(aws_config_file))


def exit_cleanup(signal, frame):
    curses.endwin()
    sys.exit(0)
