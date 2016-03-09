from django.http import HttpResponse
import session_header.middleware


class TestSessionMiddleware(object):
    def test_init(self):
        """The SessionStore should create an instance with csrf_exempt."""
        middleware = session_header.middleware.SessionMiddleware()
        store = middleware.SessionStore()
        assert not store.csrf_exempt

    def test_process_request_normal(self, rf):
        """Should not be CSRF exempt by default."""
        middleware = session_header.middleware.SessionMiddleware()
        request = rf.post('/')
        middleware.process_request(request)
        assert not request.session.csrf_exempt

    def test_process_request_header(self, rf):
        """Should be CSRF exempt with session header."""
        middleware = session_header.middleware.SessionMiddleware()
        request = rf.post('/')
        request.META['HTTP_X_SESSIONID'] = 'abcdefghijklmnopqrstuvwxyz'
        middleware.process_request(request)
        assert request.session.csrf_exempt

    def test_process_response_session_empty(self, rf):
        """There should be no sessionid header if the session is empty."""
        middleware = session_header.middleware.SessionMiddleware()
        request = rf.get('/')
        middleware.process_request(request)
        response = HttpResponse()
        response = middleware.process_response(request, response)
        assert 'X-SessionID' not in response

    def test_process_response_session_nonempty(self, rf):
        """There should be a sessionid header if the session is not empty."""
        middleware = session_header.middleware.SessionMiddleware()
        request = rf.get('/')
        middleware.process_request(request)
        response = HttpResponse()
        request.session['spam'] = 'eggs'
        response = middleware.process_response(request, response)
        assert 'X-SessionID' in response
