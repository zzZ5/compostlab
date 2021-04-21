from django.contrib.auth import login
from account.serializers import BriefUserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    """
    login(request, user)
    return {
        'user': BriefUserSerializer(user, context={'request': request}).data,
        'token': 'JWT ' + token
    }
