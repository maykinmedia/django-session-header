from rest_framework.authentication import SessionAuthentication


class SessionTokenAuthentication(SessionAuthentication):
    """
    Use SessionToken sessions for authentication.
    """

    def enforce_csrf(self, request):
        """
        Don't enforce CSRF if using a session_token.
        """
        if request.session.loaded_from_session_token():
            return
        super(SessionTokenAuthentication, self).enforce_csrf(self, request)
