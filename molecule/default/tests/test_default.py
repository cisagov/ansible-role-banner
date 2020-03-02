"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["openssh-server"])
def test_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize(
    "file,contents",
    [
        ("/etc/motd", "CYBER + INFRASTRUCTURE"),
        # Yes, the two spaces after 'information' are really intentional.
        # See files/issue.
        ("/etc/issue", "U.S. Government information  system"),
        ("/etc/ssh/sshd_config", "^Banner /etc/issue"),
    ],
)
def test_files_exist(host, file, contents):
    """Test that config files were modified as expected."""
    f = host.file(file)

    assert f.exists
    assert f.contains(contents)
