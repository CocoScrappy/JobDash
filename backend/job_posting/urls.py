from rest_framework import routers
from . import views

jobpost_router = routers.DefaultRouter()
jobpost_router.register(r'postings/default', views.DefaultJobPostView, 'posting')
jobpost_router.register(r'postings', views.JobPostView, 'posting')