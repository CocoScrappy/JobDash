from django.test import TestCase
from ..models import Application, Saved_Date
from job_posting.models import JobPost
from user.models import UserAccount
from application.models import Application, Saved_Date
from cv_basic.models import CvBasic


class ApplicationTestCase(TestCase):

    def setUp(self):
        self.recruiter = UserAccount.objects.create(
            first_name='recruiter',
            last_name='recruiter_lastname',
            email='recruiter@email.com',
            summary='Some summary',
            role='employer'
        )

        self.applicant = UserAccount.objects.create(
            first_name='applicant',
            last_name='applicant_lastname',
            email='applicant@email.com',
            summary='Some summary',
            role='user'
        )

        self.jobpost = JobPost.objects.create(
            employer=self.recruiter,
            title="Job 1",
            location="Montreal",
            description="Programming job",
            company="ACME",
            remote_option='remote'
        )

        self.cv = CvBasic.objects.create(
            user=self.applicant,
            name="My CV",
            content="cv content"
        )

        self.application = Application.objects.create(
            job_posting=self.jobpost,
            cv=self.cv,
            applicant=self.applicant,
        )

        # self.saved_date = Saved_Date.objects.create(
        #     application=self.application,
        #     name="first interview",
        #     datetime='2023-01-08 15:00:00.000000'
        # )

    def test_application_is_created_with_correct_fields(self):
        '''
        A user can register a new alication
        '''
        test_application = Application.objects.get(pk=self.application.id)
        self.assertEqual(test_application, self.application)
        self.assertEqual(test_application.applicant.email,
                         self.applicant.email)
        self.assertEqual(test_application.job_posting.title,
                         self.jobpost.title)
        self.assertEqual(
            test_application.job_posting.employer.email, self.recruiter.email)
        self.assertEqual(test_application.cv.name, self.cv.name)

    def test_applicant_already_applied_should_raise_exception(self):
        '''
        A user cannot apply to the same application twice.
        This test should return an exception
        '''
        with self.assertRaises(Exception):
            Application.objects.create(
                job_posting=self.jobpost,
                cv=self.cv,
                applicant=self.applicant,
            )
