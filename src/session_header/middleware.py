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
        sessionid = request.META.get('HTTP_X_SESSIONID')
        if sessionid:
            request.session = self.SessionStore(sessionid)
            request.session.csrf_exempt = True


class CsrfViewMiddleware(csrf.CsrfViewMiddleware):
    def process_request(self, request):
        if not request.session.csrf_exempt:
            super(CsrfViewMiddleware, self).process_request(request)


class SessionHeaderMixin(object):
    def __init__(self, session_key=None):
        super(SessionHeaderMixin, self).__init__(session_key)
        self.csrf_exempt = False
