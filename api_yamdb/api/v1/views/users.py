from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.permissions import IsAdmin
from api.v1.serializers.users import (AuthSerializer, TokenSerializer,
                                      UserSerializer)
from api_yamdb.settings import DEFAULT_EMAIL_SUBJECT, DEFAULT_FROM_EMAIL
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.data['username']
    email = serializer.data['email']
    user, _ = User.objects.get_or_create(email=email, username=username)

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        from_email=DEFAULT_FROM_EMAIL,
        message=f'Ваш код подтверждения: {confirmation_code}',
        recipient_list=[user.email],
        subject=DEFAULT_EMAIL_SUBJECT,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_check(request):
    serializer = TokenSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )

    confirmation_code = serializer.validated_data['confirmation_code']

    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        data = {'token': str(refresh.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
