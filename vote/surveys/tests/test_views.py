import os
import tempfile

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Survey
from ..serializers import SurveySerializer

from PIL import Image

SURVEY_URL = reverse('survey:survey-list')


def image_upload_url(survey_id):
    """Return URL for the survey image upload."""
    return reverse('survey:survey-upload-image', args=[survey_id])


def detail_url(survey_id):
    """Return the url of a specific survey based on its id."""
    return reverse('survey:survey-detail', args=[survey_id])


class SurveyAPITest(TestCase):
    """Test the survey available API."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_survey(self):
        """Test survey can be retrieved."""
        Survey.objects.create(
            first_name='Leon',
            last_name='Brown',
            is_us_citizen=True,
            is_registered_to_vote=True
        )
        Survey.objects.create(
            first_name='Anna',
            last_name='Montana',
            is_us_citizen=True,
            is_registered_to_vote=False
        )
        # Get API response
        res = self.client.get(SURVEY_URL)

        # Get data from databse
        surveys = Survey.objects.all().order_by('last_name')
        serializer = SurveySerializer(surveys, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_survey_succesfully(self):
        """Test survey is creatd succesfully."""
        payload = {'first_name': 'Paola',
                   'last_name': 'Anderson',
                   'is_us_citizen': False,
                   'is_registered_to_vote': False,
                   }
        self.client.post(SURVEY_URL, payload)
        exist = Survey.objects.filter(
            first_name=payload['first_name'],
            last_name=payload['last_name'],
            is_us_citizen=payload['is_us_citizen'],
            is_registered_to_vote=payload['is_registered_to_vote']
        ).exists

        self.assertTrue(exist)

    def test_create_survey_with_invalid_first_name(self):
        """Test cannot create survey with invalid first_name."""
        payload = {'first_name': '',
                   'last_name': 'Julian',
                   'is_us_citizen': False,
                   'is_registered_to_vote': False,
                   }
        res = self.client.post(SURVEY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_survey_with_invalid_last_name(self):
        """Test cannot create survey with invalid last_name."""
        payload = {'first_name': 'Jhonny',
                   'last_name': '',
                   'is_us_citizen': False,
                   'is_registered_to_vote': False,
                   }
        res = self.client.post(SURVEY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_survey_detail(self):
        """Test a survey detail can be viewed."""
        survey = Survey.objects.create(
            first_name='Jhonny',
            last_name='Juliano',
            is_us_citizen=False,
            is_registered_to_vote=False,

        )
        url = detail_url(survey.id)

        res = self.client.get(url)
        serializer = SurveySerializer(survey)

        self.assertEqual(res.data, serializer.data)


class SurveyImageUploadTest(TestCase):
    """Test uploading image enpoint."""

    def setUp(self):
        self.client = APIClient()
        self.survey = Survey.objects.create(
            first_name='Jhonny',
            last_name='Juliano',
            is_us_citizen=False,
            is_registered_to_vote=False,
        )

    def tearDown(self):
        self.survey.image.delete()

    def test_upload_image_to_survey(self):
        """Test uploading an image to survey."""
        url = image_upload_url(self.survey.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

            self.survey.refresh_from_db()
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIn('image', res.data)
            self.assertTrue(os.path.exists(self.survey.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.survey.id)
        res = self.client.post(
            url, {'image': 'notimage'}, format='multipart'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
