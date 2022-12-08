from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Application
from job_posting.models import JobPost
from user.models import UserAccount
from application.models import Application
from cv_basic.models import CvBasic
from rest_framework_simplejwt.tokens import RefreshToken


class ApplicationViewsTest(APITestCase):
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

    def test_user_can_post_new_applications(self):
        '''
        User can post a new application through api url /api/applications/; 
        Response status would be 201 and number of applications in the database should increase by 1
        '''
        client = APIClient()
        client.force_authenticate(user=self.applicant2)
        initial_applications_list = Application.objects.all()
        initial_count = len(initial_applications_list)
        response = client.post('/api/applications/', {'job_posting': self.jobpost.id,
                                                      'cv': self.cv2.id,
                                                      'applicant': self.applicant2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_application_id = response.data['id']
        new_application_from_db = Application.objects.get(
            id=new_application_id)
        self.assertEqual(response.data['cv'], new_application_from_db.cv.id)
        new_applications_list = Application.objects.all()
        new_count = len(new_applications_list)
        self.assertTrue(new_count, initial_count)

    def test_applicant_already_applied_should_raise_exception(self):
        '''
        A user cannot apply to the same application twice.
        This test should return an exception
        '''
        refresh = RefreshToken.for_user(self.applicant1)
        token = {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
        initial_applications_list = Application.objects.all()
        initial_count = len(initial_applications_list)
        response = self.client.post('/api/applications/', data={'job_posting': self.jobpost.id,
                                                                'cv': self.cv2.id,
                                                                'applicant': self.applicant2.id}, **token, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'You already applied to this job posting')
        new_applications_list = Application.objects.all()
        new_count = len(new_applications_list)
        self.assertTrue(new_count, initial_count)

    def test_user_can_view_their_own_applications(self):
        '''
        Applicant1 can view their own application1; 
        Response status would be 200
        '''
        refresh = RefreshToken.for_user(self.applicant1)
        token = {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
        url = '/api/applications/{}/details/'.format(self.application1.id)
        response = self.client.get(url, **token)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_view_other_users_applications(self):
        '''
        applicant2 cannot view application of applicant1 (application1); 
        response status would be 401
        '''
        refresh = RefreshToken.for_user(self.applicant2)
        # token of user 2
        token = {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
        # aplication of user 1
        url = '/api/applications/{}/details/'.format(self.application1.id)
        # user 2 trying to view application of user 1
        response = self.client.get(url, **token)
        # should return unauthorized status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_view_applications(self):
        '''
        A user cannot view application details without being logged in
        '''
        url = '/api/applications/{}/details/'.format(self.application1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
