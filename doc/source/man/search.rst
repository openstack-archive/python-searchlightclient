======
Search
======

search facet list
-----------------

List Searchlight Facets.

.. program:: search facet list
.. code:: bash

    openstack search facet list
        [--type <resource-type>]
        [--limit-terms <limit>]
        [--all-projects]

.. option:: --type <resource-type>

    Get facets for a particular resource type.

.. option:: --limit-terms <limit>

    Restricts the number of options returned for fields that
    support facet terms.

.. option:: --all-projects

    Request facet terms for all projects (admin only).

search resource type list
-------------------------

List Searchlight Resource Type (Plugin).

.. program:: search resource type list
.. code:: bash

    openstack search resource type list

search query
------------

Search Searchlight resource.

.. program:: search query
.. code:: bash

    openstack search query
    --type [<resource-type> [<resource-type> ...]]
    --all-projects
    --source [[<field>,...]]
    --json
    <query>

.. option:: --type [<resource-type> [<resource-type> ...]]

    One or more types to search. Uniquely identifies
    resource types. Example: ``--type OS::Glance::Image
    OS::Nova::Server``

.. option:: --all-projects

   By default searches are restricted to the current project
   unless all_projects is set.

.. option:: --source [[<field>,...]]

    Whether to display the json source. If not specified,
    it will not be displayed. If specified with no argument,
    the full source will be displayed. Otherwise, specify
    the fields combined with ',' to return the fields you want.
    It is recommended that you use the ``--max-width`` argument
    with this option.

.. option:: --json

    Treat the query argument as a JSON formatted DSL query.
