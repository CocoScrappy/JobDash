from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserSerializer, UserDashboardSerializer
from cv_basic.serializers import CvSerializer
from application.serializers import ApplicationSerializerForDashboard, SavedDatesSerializer
from cv_basic.models import CvBasic
from application.models import Application, Saved_Date
from .models import UserAccount


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        '''first_name=data['first_name']
        last_name=data['last_name']
        email=data['email']
        password=data['password']'''

        '''serializer = UserCreateSerializer(data={
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'password':password,
        })'''
        serializer = UserCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)


class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_200_OK)


class UsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserAccount.objects.all()


class UserDashboardView(APIView):
    """
        Returns info for user dashboard
        Includes user name, Cv, application with application saved_dates

        **Context**

        ``def get(self, request)``
        request.user used to get info via token

    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        cv = CvBasic.objects.get(user=user.id)
        applications = Application.objects.filter(applicant=user.id)

        # get applications, get dates, put applications IN dates and dates in user
        apps = []
        user = UserDashboardSerializer(user).data
        for a in applications:
            app = ApplicationSerializerForDashboard(a).data
            app['saved_dates'] = SavedDatesSerializer(
                a.saved_dates, many=True).data

            apps.append(app)

        user['applications'] = apps
        cv = CvSerializer(cv).data
        user['cv'] = cv
        return Response(user, status=status.HTTP_200_OK)
