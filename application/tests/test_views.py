from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Application, Saved_Date
from job_posting.models import JobPost
from user.models import UserAccount
from application.models import Application, Saved_Date
from cv_basic.models import CvBasic
from rest_framework.authtoken.models import Token
import json


class ApplicationDetailsTest(APITestCase):
    def setUp(self):
        self.recruiter = UserAccount.objects.create(
            first_name='recruiter',
            last_name='recruiter_lastname',
            email='recruiter@email.com',
            summary='Some summary',
            role='employer'
        )

        self.jobpost = JobPost.objects.create(
            employer=self.recruiter,
            title="Job 1",
            location="Montreal",
            description="Programming job",
            company="ACME",
            remote_option='remote'
        )

        self.applicant1 = UserAccount.objects.create(
            first_name='applicant',
            last_name='applicant_lastname',
            email='applicant@email.com',
            summary='Some summary',
            role='user',
            password="passwordIsCool"
        )

        self.applicant2 = UserAccount.objects.create(
            first_name='applicant2',
            last_name='applicant2_lastname',
            email='applicant2@email.com',
            summary='Some summary',
            role='user',
            password="passwordIsCool"
        )

        self.cv1 = CvBasic.objects.create(
            user=self.applicant1,
            name="My CV",
            content="cv content"
        )

        self.cv2 = CvBasic.objects.create(
            user=self.applicant2,
            name="My CV",
            content="cv content"
        )

        self.application1 = Application.objects.create(
            job_posting=self.jobpost,
            cv=self.cv1,
            applicant=self.applicant1,
        )

        # self.application2 = Application.objects.create(
        #     job_posting=self.jobpost,
        #     cv=self.cv2,
        #     applicant=self.applicant2,
        # )

        # self.saved_date1 = Saved_Date.objects.create(
        #     application=self.application1,
        #     name="first interview",
        #     datetime='2023-01-08 15:00:00.000000'
        # )

        # self.saved_date2 = Saved_Date.objects.create(
        #     application=self.application2,
        #     name="first interview",
        #     datetime='2023-01-08 15:00:00.000000'
        # )

    def test_user_can_get_their_applications(self):
        client = APIClient()
        client.force_authenticate(user=self.applicant2)
        response = client.post('/api/applications/', {'job_posting': self.jobpost.id,
                                                      'cv': self.cv2.id,
                                                      'applicant': self.applicant2.id}, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data in Application.objects.filter(
            applicant=self.applicant2))

    def test_user_can_only_view_their_own_applications(self):
        url = '/api/applications/{}/details/'.format(self.application1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
