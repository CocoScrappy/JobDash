from rest_framework import routers
from . import views
from django.urls import path

application_router = routers.DefaultRouter()
# application_router.register(r'applications/default', views.DefaultApplicationView, 'application')
application_router.register(
    r'applications', views.ApplicationView, 'application')

# urlpatterns = [
#     path('applications/search/', views.ApplicationSearchView.as_view())
# ]
