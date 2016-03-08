from __future__ import unicode_literals
from django.middleware import csrf
from django.contrib.sessions import middleware


class SessionMiddleware(middleware.SessionMiddleware):
    def __init__(self):
        super(SessionMiddleware, self).__init__()
        bases = (SessionHeaderMixin, self.SessionStore)
        self.SessionStore = type('SessionStore', bases, {})

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


class SessionHeaderMixin(object):
    """
    Extend any SessionStore class with SessionHeader behavior.
    """

    def __init__(self, session_key=None, from_header=False):
        super(SessionHeaderMixin, self).__init__(session_key)
        self.__from_header = from_header

    def loaded_from_header(self):
        """
        Determine if this request was loaded via session header.
        """
        return bool(self.__from_header)
