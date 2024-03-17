from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import RegisterForm

import jwt, datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers

dataTxt = {
    # In the form(on the right)
    'obj_message_titles':{
        'hello': 'Привет!',
        'hello_question': 'Привет! Здесь впервые?',
        'about': 'О проекте',
        'contacts': 'Контакты',
    },
    'obj_contacts_info':{
        'txt_message':'Наше Веб-приложение, разработано с целью повысить ваши профессиональные навыки', # About.html call
        'author_name':'Автор: Ilya Borisov-Bisec',
        'email':'Почта: ilya.borisov.bisec@gmail.com',
        'phone_number':'Телефон:(29)4911431 - Belarus',
    },
    'obj_tab_titles':{
        # Generally
        'main_page':'Главная страница',
        'about_page':'О проекте',
        'contacts_page':'Контакты',
        'exit_page':'Выйти',
        # Auth
        'not_registered_page': 'Добро пожаловать!',
        'login_page': 'Авторизация',
        'signup_page': 'Регистрация',
    }
}


@login_required
def home(request):
    return render(request, 'main/main.html', dataTxt)

def about(request):
    return render(request, 'main/about.html', dataTxt)

def contacts(request):
    return render(request, 'main/contacts.html', dataTxt)

def logout_view(request):
    return render(request, 'main/not_registered.html', dataTxt)




# JWT TOKEN REGISTRATION

# Custom jwt
'''class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        #render(request, 'main/login.html', dataTxt)

        email = request.data['email']
        password = request.data['password']

        user = DemoAUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = DemoAUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }
        #render(request, 'main/not_registered.html', dataTxt)
        return response'''


#from .models import Profile

User = get_user_model()

class UserRegisterationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)

class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user