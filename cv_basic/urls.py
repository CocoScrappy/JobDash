from rest_framework import routers
from django.urls import path
from cv_basic import views

cv_router = routers.DefaultRouter()
cv_router.register(r'cvs', views.CvsView, 'cv')


# urlpatterns = [
#     path('cvs/get_user_cvs', views.CvsView),
# ]

