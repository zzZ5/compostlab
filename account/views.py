from account.serializers import BriefUserSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, mixins, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView


# def jwt_response_payload_handler(token, user=None, request=None):
#     """
#     Returns the response data for both the login and refresh views.
#     Override to return a custom response such as including the
#     serialized representation of the User.
#     """
#     login(request, user)
#     return {
#         'user': BriefUserSerializer(user, context={'request': request}).data,
#         'token': 'JWT ' + token
#     }


class CreateUser(APIView):
    '''
    Create a new User, must have administrator privileges.
    '''

    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, version, format=None):
        '''
        Create a new account through post.
        Example:
            username:test1
            email:test1@example.com
            password:test123
            is_staff:true
            is_superuser:false
        Return:
            if success, return user's profile.
        '''

        serializer = UserSerializer(data=request.data)
        response_dict = {'code': 200, 'message': 'ok', 'data': []}
        if serializer.is_valid():
            serializer.save()
            response_dict['code'] = 201
            response_dict['message'] = 'Created successfully!'
            response_dict['data'] = serializer.data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        response_dict['code'] = 422
        response_dict['message'] = serializer.errors
        return Response(response_dict, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserView(mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               generics.GenericAPIView):
    '''
    Get user's profile or update user's profile through user's id.
    '''

    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = BriefUserSerializer

    def get(self, request, version, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, version, pk, *args, **kwargs):
        if request.user.id == pk:
            return self.update(request, *args, **kwargs)
        return Response(data={'detail': 'Inconsistent users'}, status=status.status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def log_out(request, version):
    '''
    Logout user.
    '''

    logout(request)
    return Response(data={'detail': 'Logout seccess!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def change_password(request, version):
    '''
    Change user's password.
    '''
    try:
        user = authenticate(
            username=request.POST.get('username'), password=request.POST.get('password'))
        if request.user != user:
            return Response(data={'detail': 'Inconsistent users'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.POST.get('new_password'))
        user.save()
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
