from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from .serializers import (
    AuthSerializer,
    OtpSerializer,
    PasswordSerializer,
    UserExistsSerializer, UserSerializer,
)
from .services.auth import AuthService, Action

User = get_user_model()


class UserExistsView(APIView):
    """
        Checks phone number is registered or Not.
        Unregistered phone number advised to go register page, else otherwise
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = UserExistsSerializer

    @swagger_auto_schema(
        request_body=UserExistsSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                title="exists"
            ),
        },
        tags=['auth'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data.get('phone_number')
        user_exists = User.objects.filter(phone_number=phone_number).exists()
        return Response({"exists": user_exists}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    serializer_class = AuthSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=AuthSerializer,
        tags=['auth'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_exists = User.objects.filter(
            Q(phone_number=serializer.data.get('phone_number')) |
            Q(phone_number2=serializer.data.get('phone_number'))
        ).exists()
        if user_exists:
            return Response({"message": _("already registered")}, status=status.HTTP_406_NOT_ACCEPTABLE)

        auth = AuthService(action=Action.REGISTER, **serializer.validated_data)
        otp = auth.register()

        # We need to get otp in response, otherwise, it must be sent to phone_number
        return Response({"otp": otp, "message": _("otp sent")}, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OtpSerializer

    @swagger_auto_schema(
        request_body=OtpSerializer,
        tags=['auth'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth = AuthService(
            phone_number=serializer.validated_data.get('phone_number'),
            action=Action.REGISTER
        )
        try:
            auth.verify(serializer.validated_data.get('otp'))
            auth.create_user()
            return Response({"message": _("otp verified")}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"message": _("otp not found")}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": _("invalid otp")}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            #  logging.error(f"{e}")
            print(e)
            return Response({"message": "Error occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = AuthSerializer

    @swagger_auto_schema(
        request_body=AuthSerializer,
        tags=['auth'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            Q(phone_number=serializer.data.get('phone_number')) |
            Q(phone_number2=serializer.data.get('phone_number'))
        ).last()

        if user and user.check_password(serializer.validated_data.get('password')):
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK
            )

        return Response({"message": _("invalid login or password")}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    serializer_class = TokenBlacklistSerializer

    @swagger_auto_schema(
        request_body=TokenBlacklistSerializer,
        tags=['auth']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": _("logged out")}, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    serializer_class = PasswordSerializer

    @swagger_auto_schema(
        request_body=PasswordSerializer,
        tags=['auth'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data.get('password'))
        request.user.save()
        return Response({"message": _("password changed")}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        return Response()


class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        return Response()


class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        request_body=UserSerializer,
        tags=['user']
    )
    def update(self, request, *args, **kwargs):
        # TODO: if phone_number changes, must be sent otp message to this phone_number
        #       logic built wrong, I think
        return super(UserView, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserSerializer,
        tags=['user']
    )
    def partial_update(self, request, *args, **kwargs):
        # TODO: if phone_number changes, must be sent otp message to this phone_number
        #       logic built wrong, I think
        return super(UserView, self).partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['user'])
    def get(self, request, *args, **kwargs):
        return super(UserView, self).get(request, *args, **kwargs)
