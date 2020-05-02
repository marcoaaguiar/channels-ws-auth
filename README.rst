=============================
Django Channels WebSocket Authentication
=============================

.. image:: https://badge.fury.io/py/channels-ws-auth.svg
    :target: https://badge.fury.io/py/channels-ws-auth

.. image:: https://travis-ci.org/marcoaaguiar/channels-ws-auth.svg?branch=master
    :target: https://travis-ci.org/marcoaaguiar/channels-ws-auth

.. image:: https://codecov.io/gh/marcoaaguiar/channels-ws-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/marcoaaguiar/channels-ws-auth

A simle and efficient WebSocket Authentication implementation for Django Channels

Documentation
-------------

The full documentation is at https://channels-ws-auth.readthedocs.io.

Quickstart
----------

Install Django Channels WebSocket Authentication::

    pip install channels-ws-auth

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'channels_ws_auth.apps.ChannelsWsAuthConfig',
        ...
    )

Add Django Channels WebSocket Authentication's URL patterns:

.. code-block:: python

    from channels_ws_auth import urls as channels_ws_auth_urls


    urlpatterns = [
        ...
        url(r'^', include(channels_ws_auth_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
