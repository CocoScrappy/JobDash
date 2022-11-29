from rest_framework import routers
from . import views

application_router = routers.DefaultRouter()
# application_router.register(r'applications/default', views.DefaultApplicationView, 'application')
application_router.register(r'applications', views.ApplicationView, 'application')