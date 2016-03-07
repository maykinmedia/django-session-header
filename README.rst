Django Session Header: Identify the session through a header
============================================================

There are some situations where the browser
may not allow any cookies at all to be used.
In those cases, we would like to be able to fall back
to something that is both secure, and capable.
This package allows you to manually pass the
sessionid using a header, so that you can continue
to use Django's excellent session management.

It extends Django's built-in sessions to support
sessions in places where cookies are not allowed.
For most views, the handling will be seamless.
Those that need to have sessions that persist despite the
absence of cookies, there are a few extra features.


Usage
=====

First, install the package.

.. code-block:: sh

    pip install django-session-header

Replace ``django.contrib.sessions.middleware.SessionMiddleware``
in your ``settings.py`` with the following:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
       # ...
       # 'django.contrib.session.middleware.SessionMiddleware',
       'session_header.middleware.SessionMiddleware',
    ]

And replace the Django Rest Framework ``SessionAuthentication``
class with ``session_header.authentication.SessionAuthentication``:

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAUlT_AUTHENTICATION_CLASSES': [
            # ...
            # 'rest_framework.authentication.SessionAuthentication',
            'session_header.authentication.SessionAuthentication',
        ]
    }

To obtain the session token to put in the body of the request,
call ``request.session.get_sessionid()``.
If the token doesn't already exist,
it will dynamically create one.

To check if a session was obtained via session header,
call ``request.session.loaded_from_header()``.
You can use this to conditionally apply CSRF protection.
Or, if you prefer, you can replace Django's normal CSRF middleware
with ``session_header.middleware.CsrfViewMiddleware``:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        # ...
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'session_header.middleware.CsrfViewMiddleware',
    ]

In order to use the template tag, you must add the
app to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'session_header',
    ]

And use the template tag in your templates like so:

.. code-block::

    {% load session_header %}
    <html data-sessionid="{% sessionid %}"></html>

Then when making your AJAX requests, just include the
``X-SessionID`` header, with that value, which you
can get using jQuery:

.. code-block::

    var sessionToken = $('html').data('sessionid')
