from fabric import Connection
from invoke import Responder
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import yaml


with open('conf.yaml', 'r') as conf_f:
    conf_s = conf_f.read()
    conf_obj = yaml.load(conf_s, Loader=Loader)


gitusername = Responder(
    pattern=r'Username for .*{host}.*'.format(host=conf_obj['git']['host']),
    response='{}\n'.format(conf_obj['git']['username']),
)
gitpassword = Responder(
    pattern=r'Password for .*{host}.*'.format(host=conf_obj['git']['host']),
    response='{}\n'.format(conf_obj['git']['password']),
)

conn = Connection(
    host=conf_obj['connection']['host'],
    user=conf_obj['connection']['username'],
    port=conf_obj['connection']['port'])
with conn.cd(conf_obj['git']['path']):
    corrent_branch = conn.run(
        "git branch | grep \\* | cut -d ' ' -f2",
        hide='stdout')
    pull_res = conn.run(
        'git pull', pty=True, watchers=[gitusername, gitpassword],
        hide='stdout')

print('* Corrent Branch: \r\n{}'.format(corrent_branch.stdout))
print('* Pull Result: \r\n{}'.format(pull_res.stdout))
