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
       'session_token.middleware.SessionTokenMiddleware',
    ]

And replace the Django Rest Framework ``SessionAuthentication``
class with:

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAUlT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionTokenAuthentication',
            'rest_framework.authentication.BasicAuthentication'
        ]
    }

Finally, in order to use the template tag, you must add the
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
