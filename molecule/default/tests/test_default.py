import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', [
    'openssh-server'
])
def test_packages(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize('file,contents', [
    ('/etc/motd', "|.   '|'   ..|'''.|     |     |''||''|  .|'''.|"),
    # Yes, the two spaces after 'information' are really intentional.
    # See files/issue.
    ('/etc/issue', 'U.S. Government information  system'),
    ('/etc/ssh/sshd_config', '^Banner /etc/issue'),
])
def test_files_exist(host, file, contents):
    f = host.file(file)

    assert f.exists
    assert f.contains(contents)
