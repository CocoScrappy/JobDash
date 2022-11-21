from rest_framework import routers
from . import views

job_posting_router = routers.DefaultRouter()
job_posting_router.register(r'postings', views.PostingView, 'posting')