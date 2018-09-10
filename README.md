Potemkin
========

A pretend LMS for testing LTI apps in development environments.

You Will Need
-------------

* Git
* Python 3.6
* Make
* SQLite
* [Tox](https://tox.readthedocs.io/en/latest/) and [tox-pip-extensions](https://github.com/tox-dev/tox-pip-extensions)

Installation & Usage
--------------------

TODO: Instructions for installing and launching from pip.

Hacking
-------

To install and run a development version of Potemkin, so you can hack on
Potemkin's own code:

```ShellSession
$ git clone git@github.com:seanh/potemkin.git
$ cd potemkin
$ make dev
```

Open <http://localhost:6543> in a browser.

To launch a Python shell in a Python environment with Potemkin and its
dependencies installed:

```ShellSession
$ make shell
```

To launch an SQL shell connected to Potemkin's development database:

```ShellSession
$ make sql
```
