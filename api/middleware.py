import re

from rest_framework.authentication import TokenAuthentication

token_pattern = re.compile(r'Token [A-z0-9]{40}')


def request_authorization_matches_pattern(request, pattern):
    return re.match(pattern, request.META['HTTP_AUTHORIZATION']) if 'HTTP_AUTHORIZATION' in request.META else False


class TokenAuthenticationMiddleware(object):

    auth = TokenAuthentication()

    def resolve(self, next, root, info, **kwargs):
        if info.context.user.is_anonymous and request_authorization_matches_pattern(info.context, token_pattern):
            (info.context.user, _) = self.auth.authenticate(info.context)
        return next(root, info, **kwargs)
