from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Accounts
from .serializers import AccountsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


@api_view(["POST"])
def register(request):
    """Kullanıcı kayıt fonksiyonu"""
    name = request.data.get("name")
    surname = request.data.get("surname")
    email = request.data.get("email")
    password = request.data.get("password")

    if not name or not surname or not email or not password:
        return Response(
            {"error": "Hatalı veya eksik bilgi girdiniz"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = AccountsSerializer(
        data={
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,
        }
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8 or len(password) > 16:
        return Response(
            {"error": "Şifre 8-16 karakter arasında olmalıdır"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if Accounts.objects.filter(email=email).exists():
            return Response(
                {"error": "Bu email adresi zaten kullanılıyor"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        account = Accounts.objects.create(
            name=name,
            surname=surname,
            email=email,
            password=ph.hash(password),
        )

        token = AccessToken.for_user(account)
        refresh = RefreshToken.for_user(account)

        return Response(
            {
                "account": serializer.data,
                "token": str(token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    """Kullanıcı giriş fonksiyonu"""
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        account = Accounts.objects.get(email=email)

        if ph.verify(account.password, password):
            token = AccessToken.for_user(account)
            refresh = RefreshToken.for_user(account)
            return Response(
                {
                    "token": str(token),
                    "refresh": str(refresh),
                },
            )
        else:
            return Response(
                {"error": "Şifre veya email adresi hatalı"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Accounts.DoesNotExist:
        return Response(
            {"error": "Bu email adresi bulunamadı"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except VerifyMismatchError as e:
        return Response(
            {"error": "Şifre veya email adresi hatalı"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_info(request):
    """Kullanıcı bilgileri fonksiyonu"""
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        access_token = AccessToken(token)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    account = access_token.payload.get("user_id", None)
    if not account:
        return Response(
            {"error": "Kullanıcı bulunamadı"}, status=status.HTTP_404_NOT_FOUND
        )

    account_data = AccountsSerializer(Accounts.objects.get(id=account)).data

    if not account_data:
        return Response(
            {"error": "Kullanıcı bulunamadı"}, status=status.HTTP_404_NOT_FOUND
        )

    return Response(account_data, status=status.HTTP_200_OK)
