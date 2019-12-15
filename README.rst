========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/python-searchlightclient.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

========================
python-searchlightclient
========================

OpenStack Indexing and Search API Client Library

This is a client library for Searchlight built on the Searchlight API. It
provides a Python API (the ``searchlightclient`` module) and a command-line
tool (``searchlight``).

The project is hosted on `Storyboard`_, where bugs can be filed. The code is
hosted on `OpenStack git repository`_. Patches must be submitted using
`Gerrit`_, *not* git repo
pull requests.

.. _OpenStack git repository: https://opendev.org/openstack/python-searchlightclient
.. _Storyboard: https://storyboard.openstack.org/#!/project_group/searchlight
.. _Gerrit: https://docs.openstack.org/infra/manual/developers.html#development-workflow

python-searchlightclient is licensed under the Apache License like the rest of
OpenStack.

.. contents:: Contents:
   :local:

Install the client from PyPI
----------------------------
The program `python-searchlightclient`_ package is published on `PyPI`_ and
so can be installed using the pip tool, which will manage installing all
python dependencies::

   $ pip install python-searchlightclient

.. note::
   The packages on PyPI may lag behind the git repo in functionality.

.. _PyPI: https://pypi.python.org/pypi/python-searchlightclient/

Setup the client from source
----------------------------

* Clone repository for python-searchlightclient::

    $ git clone https://opendev.org/openstack/python-searchlightclient.git
    $ cd python-searchlightclient

* Setup a virtualenv

.. note::
   This is an optional step, but will allow Searchlightclient's dependencies
   to be installed in a contained environment that can be easily deleted
   if you choose to start over or uninstall Searchlightclient.

::

    $ tox -evenv --notest

Activate the virtual environment whenever you want to work in it.
All further commands in this section should be run with the venv active:

::

    $ source .tox/venv/bin/activate

.. note::
   When ALL steps are complete, deactivate the virtualenv: $ deactivate

* Install Searchlightclient and its dependencies::

    (venv) $ python setup.py develop

Command-line API
----------------

Set Keystone environment variables to execute CLI commands against searchlight.

* To execute CLI commands::

    $ export OS_USERNAME=<user>
    $ export OS_PASSWORD=<password>
    $ export OS_TENANT_NAME=<project>
    $ export OS_AUTH_URL='http://localhost:5000/v2.0/'

.. note::
   With devstack you just need to $ source openrc <user> <project>. And you can
   work with a local installation by passing --os-token <TOKEN> and --os-url
   http://localhost:9393. You can also set up a `Openstackclient`_ config file
   to work with the CLI.

.. _Openstackclient: https://docs.openstack.org/developer/python-openstackclient/configuration.html#clouds-yaml

::

    $ openstack
    (openstack) search resource type list
    +--------------------------+--------------------------+
    | Name                     | Type                     |
    +--------------------------+--------------------------+
    | OS::Designate::RecordSet | OS::Designate::RecordSet |
    | OS::Designate::Zone      | OS::Designate::Zone      |
    | OS::Glance::Image        | OS::Glance::Image        |
    | OS::Glance::Metadef      | OS::Glance::Metadef      |
    | OS::Nova::Server         | OS::Nova::Server         |
    +--------------------------+--------------------------+

Here are the full list of subcommands, Use -h to see options:

    ============================= =======================================
    Subcommand                    Description
    ============================= =======================================
    search facet list             List Searchlight Facet
    search resource type list     List Searchlight Resource Type (Plugin)
    search query                  Search Searchlight resource
    ============================= =======================================

Python API
----------

To use with keystone as the authentication system::

    >>> from keystoneclient.auth.identity import generic
    >>> from keystoneclient import session
    >>> from searchlightclient import client
    >>> auth = generic.Password(auth_url=OS_AUTH_URL, username=OS_USERNAME, password=OS_PASSWORD, tenant_name=OS_TENANT_NAME)
    >>> keystone_session = session.Session(auth=auth)
    >>> sc = client.Client('1', session=keystone_session)
    >>> sc.resource_types.list()
    [...]


* License: Apache License, Version 2.0
* Documentation: https://docs.openstack.org/developer/python-searchlightclient
* Source: https://opendev.org/openstack/python-searchlightclient
* Bugs: https://storyboard.openstack.org/#!/project_group/searchlight

Testing
-------

There are multiple test targets that can be run to validate the code.

* tox -e pep8 - style guidelines enforcement
* tox -e py36 - traditional unit testing with python 3.6
* tox -e py37 - traditional unit testing with python 3.7
