from rest_framework import routers
from applicant import views

applicant_router = routers.DefaultRouter()
applicant_router.register(r'applicants', views.List_Applicants_View, 'applicant')