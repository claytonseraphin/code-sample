from django.db import models

import uuid
import os


def survey_upload_file_path(instance, filename):
    """Generate file path for new person in the survey."""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/survey/', filename)


# Create your models here.


class Survey(models.Model):
    """
    Who can vote model
    Define the attributes of who can vote
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=survey_upload_file_path)
    is_us_citizen = models.BooleanField()
    is_registered_to_vote = models.BooleanField()

    def get_us_citizen(self):
        """Returns if citizen can vote or not."""
        if self.is_us_citizen and self.is_registered_to_vote:
            return self.first_name + " " + self.last_name + " " + "can vote."
        return self.first_name + " " + self.last_name + " " + "can't vote."

    def __str__(self):
        return self.first_name + self.last_name
