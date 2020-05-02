=====
Usage
=====

To use Django Channels WebSocket Authentication in a project, add it to your `INSTALLED_APPS`:

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
