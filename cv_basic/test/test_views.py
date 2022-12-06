from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from ..models import CvBasic
from job_posting.models import JobPost
from user.models import UserAccount
from application.models import Application
from cv_basic.models import CvBasic
from rest_framework_simplejwt.tokens import RefreshToken


class Cv_View_Test(APITestCase):
    def setUp(self):

        self.user1 = UserAccount.objects.create(
            first_name='user1',
            last_name='user1_lastname',
            email='user1@email.com',
            summary='Some summary',
            role='user',
            password="passwordIsCool"
        )

        self.user2 = UserAccount.objects.create(
            first_name='user2',
            last_name='user2_lname',
            email='user2@email.com',
            summary='Some summary',
            role='user',
            password="passwordIsCool"
        )

        self.cv1 = CvBasic.objects.create(
            user=self.user1,
            name="CV for user 1",
            content="cv content"
        )

    def test_user_can_post_new_cv(self):
        '''
        User can post a new cv through api url /api/cvs/;
        Response status would be 201 and number of cvs in the database should increase by 1
        '''
        client = APIClient()
        client.force_authenticate(user=self.user2)
        initial_cv_list = client.get(
            '/api/cvs/', format='json').data
        initial_count = len(initial_cv_list)
        response = client.post('/api/cvs/', {'user': self.user2.id,
                                             'name': 'CV for user 2',
                                             'content': 'Initial CV content'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_cv_list = client.get(
            '/api/cvs/', format='json').data
        new_count = len(new_cv_list)
        self.assertTrue(new_count, initial_count)

    def test_user_can_update_cv(self):
        '''
        User can update their cv through api url /api/cvs/:cvId;
        updated cv should be reflected in database
        '''
        refresh = RefreshToken.for_user(self.user1)
        token = {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}
        url = '/api/cvs/{}/'.format(self.cv1.id)
        data = {'content': 'updated cv content'}
        response = self.client.patch(url, data, **token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cv_from_db = CvBasic.objects.get(id=self.cv1.id)
        self.assertEqual(cv_from_db.content, response.data['content'])
        self.assertEqual(cv_from_db.content, 'updated cv content')
        self.assertNotEqual(cv_from_db.content, 'Initial CV content')
