from rest_framework import routers
from user import views

user_router = routers.DefaultRouter()
user_router.register(r'users/default', views.Default_Users_View, 'user')
user_router.register(r'users', views.Users_With_CV_View, 'user')