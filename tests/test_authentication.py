import pytest
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
import session_header.authentication


class TestSessionAuthentication(object):
    def test_enforce_csrf_normal(self, rf):
        """Should cause CSRF failure normally."""
        middleware = session_header.middleware.SessionMiddleware()
        authentication = session_header.authentication.SessionAuthentication()
        request = rf.post('/')
        middleware.process_request(request)
        with pytest.raises(PermissionDenied):
            authentication.enforce_csrf(Request(request))

    def test_enforce_csrf_session_header(self, rf):
        """Should not cause CSRF failure when using a header."""
        middleware = session_header.middleware.SessionMiddleware()
        authentication = session_header.authentication.SessionAuthentication()
        request = rf.post('/')
        request.META['HTTP_X_SESSIONID'] = 'abcdefghijklmnopqrstuvwxyz'
        middleware.process_request(request)
        authentication.enforce_csrf(Request(request))
