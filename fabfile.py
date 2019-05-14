import argparse
from collections import OrderedDict

from fabric import Connection
from invoke import Responder
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import yaml


def load_service(service_name=None):
    """Load the config from config file.

    Pick up the 1st service which in config file if no service pointed.
    :params service_name:
        type: string
        desc: The service name. must as same as it in config file.
    :return:
        conf_obj:
            type: OrderedDict
    """
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
    def dict_representer(dumper, data):
        return dumper.represent_dict(data.iteritems())
    def dict_constructor(loader, node):
        return OrderedDict(loader.construct_pairs(node))
    yaml.add_representer(OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)
    with open('conf.yaml', 'r') as conf_f:
        conf_s = conf_f.read()
        conf_obj = yaml.load(conf_s, Loader=Loader)
    if service_name:
        conf_obj = conf_obj.get(service_name)
    else:
        for k, _ in conf_obj.iteritems():
            if k.startswith('service_'):
                conf_obj = conf_obj[k]
                break
        else:
            conf_obj = None
            raise ValueError('Please add a service in conf file.')
    return conf_obj


parser = argparse.ArgumentParser()
parser.add_argument(
    '--service', type=str, help='The service which is in config file')
args = parser.parse_args()
service_name = args.service

conf_obj = load_service(service_name)

gitusername = Responder(
    pattern=r'Username for .*{host}.*'.format(
        host=conf_obj['git']['host']),
    response='{}\n'.format(conf_obj['git']['username']),
)
gitpassword = Responder(
    pattern=r'Password for .*{host}.*'.format(
        host=conf_obj['git']['host']),
    response='{}\n'.format(conf_obj['git']['password']),
)

conn = Connection(
    host=conf_obj['connection']['host'],
    user=conf_obj['connection']['username'],
    port=conf_obj['connection']['port'],
    connect_kwargs={'password': conf_obj['connection']['password']})
with conn.cd(conf_obj['git']['path']):
    corrent_branch = conn.run(
        "git branch | grep \\* | cut -d ' ' -f2",
        hide='stdout')
    pull_res = conn.run(
        'git pull', pty=True, watchers=[gitusername, gitpassword],
        hide='stdout')

print('* Corrent Branch: \r\n{}'.format(corrent_branch.stdout))
print('* Pull Result: \r\n{}'.format(pull_res.stdout))
