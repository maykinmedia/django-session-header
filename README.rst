Django Session Token: cookieless sessions for Django
====================================================

There are some situations where the browser
may not allow any cookies at all to be used.
In those cases, we would like to be able to fall back
to something that is both secure, and capable.
This package allows you to use a unique token
that identifies the session,
without creating a CSRF vulnerability by leaking the sessionid.

It extends Django's built-in sessions to support
sessions in places where cookies are not allowed.
For most views, the handling will be seamless.
Those that need to have sessions that persist despite the
absence of cookies, there are a few extra features.


Usage
=====

First, install the package.

.. code-block:: sh

    pip install django-session-token

Replace ``django.contrib.sessions.middleware.SessionMiddleware``
in your ``settings.py`` with the following:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
       # ...
       # 'django.contrib.session.middleware.SessionMiddleware',
       'session_token.middleware.SessionTokenMiddleware',
    ]

And replace the Django Rest Framework ``SessionAuthentication``
class with ``SessionTokenAuthentication``:

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAUlT_AUTHENTICATION_CLASSES': [
            # ...
            # 'rest_framework.authentication.SessionAuthentication',
            'session_token.authentication.SessionTokenAuthentication',
        ]
    }

To obtain the session token to put in the body of the request,
call ``request.session.get_session_token()``.
If the token doesn't already exist,
it will dynamically create one.

To check if a session wa obtained via session token,
call ``request.session.loaded_from_session_token()``.
You can use this to conditionally apply CSRF protection.
Or, if you prefer, you can replace Django's normal CSRF middleware
with ``session_token.middleware.SessionTokenCsrfViewMiddleware``:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        # ...
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'session_token.middleware.SessionTokenCsrfViewMiddleware',
    ]

In order to use the template tag, you must add the
app to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'session_token',
    ]

And use the template tag in your templates like so:

.. code-block::

    {% load session_token %}
    <html data-session-token="{% session_token %}"></html>

Then when making your AJAX requests, just include the
``X-Session-Token`` header, with that value, which you
can get using jquery:

.. code-block::

    var sessionToken = $('html').data('session-token')
