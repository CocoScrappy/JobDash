from rest_framework import routers
from cv import views

cv_router = routers.DefaultRouter()
cv_router.register(r'cvs/default', views.DefaultCvsView, 'cv')
cv_router.register(r'cvs', views.CvsView, 'cv')
cv_router.register(r'cv-elements', views.CvElementsView, 'cv-element')