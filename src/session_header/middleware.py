from __future__ import unicode_literals
from django.middleware import csrf
from django.contrib.sessions import middleware


class SessionMiddleware(middleware.SessionMiddleware):
    def __init__(self):
        super(SessionMiddleware, self).__init__()

        class SessionStore(SessionHeaderStore, self.SessionStore):
            """
            A Subclassed Session Store with Session Token abilities.
            """

        self.SessionStore = SessionStore

    def process_request(self, request):
        super(SessionMiddleware, self).process_request(request)

        session_header = request.META.get('HTTP_X_SESSIONID')
        if session_header:
            request.session = self.SessionStore(
                session_header, from_header=True)


class CsrfViewMiddleware(csrf.CsrfViewMiddleware):
    def process_request(self, request):
        if request.session.loaded_from_header():
            return
        super(CsrfViewMiddleware, self).process_request(request)


class SessionHeaderStore(object):
    """
    Extend any SessionStore class with SessionHeader behavior.
    """

    def __init__(self, session_key=None, from_header=False):
        self.__from_header = from_header
        super(SessionHeaderStore, self).__init__(session_key)

    def loaded_from_header(self):
        """
        Determine if this request was loaded via session header.
        """
        return bool(self.__from_header)

    def get_sessionid(self):
        """
        Get the current session token, or create a new one.
        """
        if not self.session_key:
            self.create()
        return self.session_key
