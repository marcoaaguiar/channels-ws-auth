# Django Channels WebSocket Authentication

[![image](https://badge.fury.io/py/channels-ws-auth.svg)](https://badge.fury.io/py/channels-ws-auth) [![image](https://travis-ci.org/marcoaaguiar/channels-ws-auth.svg?branch=master)](https://travis-ci.org/marcoaaguiar/channels-ws-auth) [![image](https://codecov.io/gh/marcoaaguiar/channels-ws-auth/branch/master/graph/badge.svg)](https://codecov.io/gh/marcoaaguiar/channels-ws-auth)

A simple and efficient WebSocket Authentication implementation for Django Channels

## How it works

This package implements a two-step message exchange protocol to achieve implement authentication on Websocket. The protocol is based on this article in [Heroku](https://devcenter.heroku.com/articles/websocket-security#authentication-authorization).
Read further down what are the advantages compared to other typically suggested approaches.

It follows the following steps:

1. The client sends a POST to `/ws-auth` (it may be desired to specify a `path`, depending on the configurations)
2. API receives the POST and creates a new Ticket on the database and returns a ticket key (uuid4).
3. The client initiates a WebSocket connection with the ticket in the query string.

The tickets are short-lived (10 seconds by default) and single-use, which ensure a certain degree of safety.

## Installation

Install Django Channels WebSocket Authentication:

```bash
pip install channels-ws-auth
```

Add it to your \`INSTALLED_APPS\`:

```python
INSTALLED_APPS = (
    ...
    'channels_ws_auth.apps.ChannelsWsAuthConfig',
    ...
)
```

Add Django Channels WebSocket Authentication's URL patterns:

```python
from channels_ws_auth import urls as channels_ws_auth_urls


urlpatterns = [
    ...
    path("ws-auth/", include("channels_ws_auth.urls", namespace="channels_ws_auth")),
    ...
]
```

## Options

The options are:

| Option                      | Default      | Description            |
| --------------------------- | ------------ | ---------------------- |
| CHANNELS_WS_AUTH_EXPIRATION | 10 (seconds) | Ticket validity period |

## Help us

New issues with bug information and Pull requests are welcome!

### Running Tests

Before performing a pull request make sure that your modifications pass in the test.

```bash
    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [cookiecutter-djangopackage](https://github.com/pydanny/cookiecutter-djangopackage)
