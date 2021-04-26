from django.test import TestCase
from unittest.mock import patch

from .. import models


class ModelTest(TestCase):
    """Test module for survey."""

    def setUp(self):
        models.Survey.objects.create(
            first_name='Reginae', last_name='Pierce',
            is_us_citizen=True, is_registered_to_vote=True
        )
        models.Survey.objects.create(
            first_name='Anthony', last_name='Louis',
            is_us_citizen=True, is_registered_to_vote=False
        )

    def test_us_citizen(self):
        """Test the US citizen eligibility to vote."""
        survey1 = models.Survey.objects.get(first_name='Reginae',
                                            last_name='Pierce'
                                            )
        survey2 = models.Survey.objects.get(
            first_name='Anthony', last_name='Louis')

        self.assertEqual(
            survey1.get_us_citizen(), "Reginae Pierce can vote."
        )
        self.assertEqual(
            survey2.get_us_citizen(), "Anthony Louis can't vote."
        )

    def test_survey_str(self):
        """Test the survey string representation."""
        survey = models.Survey.objects.create(
            first_name="Lora",
            last_name='Anderson',
            is_us_citizen=True,
            is_registered_to_vote=True,
        )

        self.assertEqual(str(survey), survey.first_name + survey.last_name)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.survey_upload_file_path(None, 'image.jpg')

        exp_path = f'uploads/survey/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
