from django.urls import path, include
from .views import RegisterView, RetrieveUserView, UsersView
from rest_framework import routers

user_router = routers.DefaultRouter()
user_router.register(r'users', UsersView, 'user')

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('me',RetrieveUserView.as_view()),
]
