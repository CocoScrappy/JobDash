from rest_framework import routers
from cv_basic import views

cv_router = routers.DefaultRouter()
cv_router.register(r'cvs', views.CvsView, 'cv')