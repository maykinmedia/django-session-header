from __future__ import unicode_literals
import string

from django.conf import settings
from django.core.cache import caches
from django.utils.crypto import get_random_string
from django.contrib.sessions.middleware import SessionMiddleware

VALID_KEY_CHARS = string.ascii_lowercase + string.digits
KEY_PREFIX = 'django-session-token.middleware'


class SessionTokenMiddleware(SessionMiddleware):
    def __init__(self):
        super(SessionTokenMiddleware, self).__init__()

        class SessionStore(SessionTokenStore, self.SessionStore):
            """
            A Subclassed Session Store with Session Token abilities.
            """

        self.SessionStore = SessionStore

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        session_token = request.META.get('HTTP_X_SESSION_TOKEN')
        if session_token:
            session_key = None
        request.session = self.SessionStore(session_key, session_token)

    def process_response(self, request, response):
        supr = super(SessionTokenMiddleware, self)
        response = supr.process_response(request, response)
        request.session._save_session_token()
        return response


class SessionTokenStore(object):
    """
    Extend any SessionStore class with SessionToken behavior.
    """

    session_token_cache_key_prefix = KEY_PREFIX

    def __init__(self, session_key=None, session_token=None):
        self.__session_token_cache = caches[settings.SESSION_CACHE_ALIAS]
        self.__session_token_saved = False
        self.session_token = session_token
        super(SessionTokenStore, self).__init__(session_key)

    def get_session_token(self):
        """
        Get the current session token, or create a new one.
        """
        if not self.session_token:
            self.session_token = self.__get_new_session_token()
        return self.session_token

    def __get_new_session_token(self):
        while True:
            session_token = get_random_string(32, VALID_KEY_CHARS)
            cache_key = self.session_token_cache_key_prefix + session_token
            if cache_key and cache_key not in self.__session_token_cache:
                break
        return session_token

    def _save_session_token(self):
        """
        Save the session token to the cache.

        Must be called after the session key is identified.
        """
        if self.session_token and not self.__session_token_saved:
            self._cache.add(self.session_token,
                            self._session_key,
                            self.get_expiry_age())
            self.__session_token_saved = True

    # Lifecycle management overrides

    def load(self):
        if self.session_token:
            cache = self.__session_token_cache
            try:
                session_key = cache.get(self.session_token)
                self.__session_token_saved = True
            except Exception:
                # Reset if an invalid session token
                self.session_token = None
                self.__session_token_saved = False
            if session_key is None:
                self.session_token = None
                self.__session_token_saved = False

        return super(SessionTokenStore, self).load()

    def create(self):
        super(SessionTokenStore, self).create()

        if self.session_token:
            self.session_token = self.__get_new_session_token()
            self.__session_token_saved = False

    def delete(self, session_key=None):
        """
        Deletes the session data under this key. If the key is None, the
        current session key value is used.
        """
        super(SessionTokenStore, self).delete(session_key=None)

        if self.session_token:
            self.session_token = None
            self.__session_token_saved = False
