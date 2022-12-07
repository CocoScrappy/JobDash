from rest_framework import routers
from . import views
from django.urls import path, include

jobpost_router = routers.DefaultRouter()
jobpost_router.register(r'postings/default',
                        views.DefaultJobPostView, 'posting')
jobpost_router.register(r'postings', views.JobPostView, 'posting')
# jobpost_router.register(r'', views.JobSearchView, 'posting')

urlpatterns = [
    path('postings/search/<str:par>/<str:loc>/', views.JobSearchView.as_view()),
    path('postings/search/<str:par>/', views.JobSearchView.as_view()),
    path('postings/analyze/', views.JobMatchView.as_view())
]
