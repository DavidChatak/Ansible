# [jenkins](#jenkins)

Install and configure jenkins on your system.

|Travis|GitHub|GitLab|Quality|Downloads|Version|
|------|------|------|-------|---------|-------|
|[![travis](https://travis-ci.com/robertdebock/ansible-role-jenkins.svg?branch=master)](https://travis-ci.com/robertdebock/ansible-role-jenkins)|[![github](https://github.com/robertdebock/ansible-role-jenkins/workflows/Ansible%20Molecule/badge.svg)](https://github.com/robertdebock/ansible-role-jenkins/actions)|[![gitlab](https://gitlab.com/robertdebock/ansible-role-jenkins/badges/master/pipeline.svg)](https://gitlab.com/robertdebock/ansible-role-jenkins)|[![quality](https://img.shields.io/ansible/quality/29474)](https://galaxy.ansible.com/robertdebock/jenkins)|[![downloads](https://img.shields.io/ansible/role/d/29474)](https://galaxy.ansible.com/robertdebock/jenkins)|[![Version](https://img.shields.io/github/release/robertdebock/ansible-role-jenkins.svg)](https://github.com/robertdebock/ansible-role-jenkins/releases/)|

## [Example Playbook](#example-playbook)

This example is taken from `molecule/resources/converge.yml` and is tested on each push, pull request and release.
```yaml
---
- name: Converge
  hosts: all
  become: yes
  gather_facts: yes

  roles:
    - role: robertdebock.jenkins
```

The machine needs to be prepared in CI this is done using `molecule/resources/prepare.yml`:
```yaml
---
- name: Prepare
  hosts: all
  gather_facts: no
  become: yes

  roles:
    - role: robertdebock.bootstrap
    - role: robertdebock.java
    - role: robertdebock.locale
    - role: robertdebock.core_dependencies
```

Also see a [full explanation and example](https://robertdebock.nl/how-to-use-these-roles.html) on how to use these roles.

## [Role Variables](#role-variables)

These variables are set in `defaults/main.yml`:
```yaml
---
# defaults file for jenkins

# What tcp port Jenkins should listen to.
jenkins_port: 8080

# What address Jenkins should bind to.
jenkins_listen_address: 0.0.0.0
```

## [Requirements](#requirements)

- pip packages listed in [requirements.txt](https://github.com/robertdebock/ansible-role-jenkins/blob/master/requirements.txt).

## [Status of requirements](#status-of-requirements)

The following roles are used to prepare a system. You may choose to prepare your system in another way, I have tested these roles as well.

| Requirement | Travis | GitHub |
|-------------|--------|--------|
| [robertdebock.bootstrap](https://galaxy.ansible.com/robertdebock/bootstrap) | [![Build Status Travis](https://travis-ci.com/robertdebock/ansible-role-bootstrap.svg?branch=master)](https://travis-ci.com/robertdebock/ansible-role-bootstrap) | [![Build Status GitHub](https://github.com/robertdebock/ansible-role-bootstrap/workflows/Ansible%20Molecule/badge.svg)](https://github.com/robertdebock/ansible-role-bootstrap/actions) |
| [robertdebock.java](https://galaxy.ansible.com/robertdebock/java) | [![Build Status Travis](https://travis-ci.com/robertdebock/ansible-role-java.svg?branch=master)](https://travis-ci.com/robertdebock/ansible-role-java) | [![Build Status GitHub](https://github.com/robertdebock/ansible-role-java/workflows/Ansible%20Molecule/badge.svg)](https://github.com/robertdebock/ansible-role-java/actions) |
| [robertdebock.locale](https://galaxy.ansible.com/robertdebock/locale) | [![Build Status Travis](https://travis-ci.com/robertdebock/ansible-role-locale.svg?branch=master)](https://travis-ci.com/robertdebock/ansible-role-locale) | [![Build Status GitHub](https://github.com/robertdebock/ansible-role-locale/workflows/Ansible%20Molecule/badge.svg)](https://github.com/robertdebock/ansible-role-locale/actions) |
| [robertdebock.core_dependencies](https://galaxy.ansible.com/robertdebock/core_dependencies) | [![Build Status Travis](https://travis-ci.com/robertdebock/ansible-role-core_dependencies.svg?branch=master)](https://travis-ci.com/robertdebock/ansible-role-core_dependencies) | [![Build Status GitHub](https://github.com/robertdebock/ansible-role-core_dependencies/workflows/Ansible%20Molecule/badge.svg)](https://github.com/robertdebock/ansible-role-core_dependencies/actions) |

## [Context](#context)

This role is a part of many compatible roles. Have a look at [the documentation of these roles](https://robertdebock.nl/) for further information.

Here is an overview of related roles:
![dependencies](https://raw.githubusercontent.com/robertdebock/drawings/artifacts/jenkins.png "Dependency")

## [Compatibility](#compatibility)

This role has been tested on these [container images](https://hub.docker.com/u/robertdebock):

|container|tags|
|---------|----|
|debian|buster|
|el|all|
|fedora|all|

The minimum version of Ansible required is 2.9, tests have been done to:

- The previous version.
- The current version.
- The development version.

## [Exceptions](#exceptions)

Some variarations of the build matrix do not work. These are the variations and reasons why the build won't work:

| variation                 | reason                 |
|---------------------------|------------------------|
| alpine | tried to configure name using a file "/etc/sysconfig/clock", but could not write to it |
| amazonlinux | /etc/rc.d/init.d/jenkins: line 59: /etc/init.d/functions: No such file or directory |
| ubuntu:bionic | No openjdk 8, with openjdk 11 jenkins returns an error. |
| ubuntu:focal | No openjdk 8, with openjdk 11 jenkins returns an error. |
| opensuse | An initscript is not idempotent. |


## [Testing](#testing)

[Unit tests](https://travis-ci.com/robertdebock/ansible-role-jenkins) are done on every commit, pull request, release and periodically.

If you find issues, please register them in [GitHub](https://github.com/robertdebock/ansible-role-jenkins/issues)

Testing is done using [Tox](https://tox.readthedocs.io/en/latest/) and [Molecule](https://github.com/ansible/molecule):

[Tox](https://tox.readthedocs.io/en/latest/) tests multiple ansible versions.
[Molecule](https://github.com/ansible/molecule) tests multiple distributions.

To test using the defaults (any installed ansible version, namespace: `robertdebock`, image: `fedora`, tag: `latest`):

```
molecule test

# Or select a specific image:
image=ubuntu molecule test
# Or select a specific image and a specific tag:
image="debian" tag="stable" tox
```

Or you can test multiple versions of Ansible, and select images:
Tox allows multiple versions of Ansible to be tested. To run the default (namespace: `robertdebock`, image: `fedora`, tag: `latest`) tests:

```
tox

# To run CentOS (namespace: `robertdebock`, tag: `latest`)
image="centos" tox
# Or customize more:
image="debian" tag="stable" tox
```

## [License](#license)

Apache-2.0


## [Author Information](#author-information)

[Robert de Bock](https://robertdebock.nl/)

Please consider [sponsoring me](https://github.com/sponsors/robertdebock).
