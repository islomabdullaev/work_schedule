from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView

from authentication.models import CustomUser
from authentication.serializers import RegisterSerializer
import jwt
import datetime


class RegisterView(GenericAPIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = CustomUser.objects.filter(
            username=username
        ).first()
        if user is None:
            raise AuthenticationFailed("User not found !")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm="HS256")

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token,
        }

        return response


class UserView(GenericAPIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated !")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        user = CustomUser.objects.filter(id=payload["id"]).first()

        serializer = RegisterSerializer(user)

        return Response(serializer.data)


class LogoutView(GenericAPIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "logged out !"
        }
        return response


