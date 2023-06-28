========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |commits-since|

.. |github-actions| image:: https://github.com/marcopist/tinksync/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/marcopist/tinksync/actions

.. |codecov| image:: https://codecov.io/gh/marcopist/tinksync/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/marcopist/tinksync

.. |commits-since| image:: https://img.shields.io/github/commits-since/marcopist/tinksync/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/marcopist/tinksync/compare/v0.0.0...main



.. end-badges

Integrate Google Sheets with Money Dashboard

* Free software: MIT license

Installation
============

::

    pip install tinksync

You can also install the in-development version with::

    pip install https://github.com/marcopist/tinksync/archive/main.zip


Documentation
=============


To use the project:

.. code-block:: python

    import tinksync
    tinksync.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
