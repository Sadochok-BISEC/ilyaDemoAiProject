from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import RegisterForm
from .models import DemoAUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer

import jwt, datetime

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

# User authentication
def login_view(request):
    return render(request, 'main/login.html', dataTxt)

class SignUpView(CreateView):
    form_class = RegisterForm
    template_name = 'main/signup.html'
    success_url = '/demoProject/home'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def signup_view(request):
    return render(request, 'main/signup.html', dataTxt)

def logout_view(request):
    return render(request, 'main/not_registered.html', dataTxt)




# JWT TOKEN REGISTRATION

class RegisterView(APIView):
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
        return response