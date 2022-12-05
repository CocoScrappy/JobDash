import sys
from django.shortcuts import render
from rest_framework import viewsets, status
from . import serializers
from rest_framework.decorators import action
from .models import JobPost
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize
import json
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.


class DefaultJobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.DefaultJobPostSerializer
    queryset = JobPost.objects.all()


class JobPostView(viewsets.ModelViewSet):
    serializer_class = serializers.JobPostSerializer
    pagination_class=LimitOffsetPagination
    queryset = JobPost.objects.all()

    @action(detail=False, methods=['get'], url_path="get_user_postings")
    def get_user_job_postings(self, request):
        try:
            user = request.user

            if (user.role == 'employer'):

                userPosts = JobPost.objects.filter(
                    employer=user.id).select_related("employer")
            else:
                userPosts = JobPost.objects.all()
            if not userPosts:
                return Response({"message": "No job postings found for current user",
                                 "data": []},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = []
                #pagination must happen before serialization
                userPosts=self.paginate_queryset(userPosts)
                for post in userPosts:
                    
                    posting = self.get_serializer(post).data
                    data.append(posting)
                print(data)
                return self.get_paginated_response(data)
                #return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return Response({"message": "WHOOPS, and error occurred; " + getattr(e, 'message', repr(e))},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobSearchView(APIView, LimitOffsetPagination):
    serializer_class = serializers.JobPostSerializer
    
    
    def get(self, request, par, loc=None):
        print(request.user, file=sys.stderr)
        user=request.user
        searchTerms = par.split()
        searchLocation=loc
        query = None
        for t in searchTerms:
            q = JobPost.objects.filter(
                Q(title__icontains=t) | Q(description__icontains=t))
            
            if searchLocation != None:
                q=q.filter(Q(remote_option__icontains=loc)|Q(location__icontains=loc))

            if user.role=='employer':
                q=q.filter(employer=user.id)

            if query == None:
                query = q
            else:
                query = query | q

        query=self.paginate_queryset(query,request,view=self)
        jsonquery = json.loads(serialize('json', query))

        print(searchTerms, file=sys.stderr)
        return LimitOffsetPagination.get_paginated_response(self,jsonquery)
        #return Response(jsonquery, status=status.HTTP_200_OK)
