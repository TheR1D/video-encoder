from uuid import uuid4

from django.db import models

from app.utils.misc import validate_file_name, validate_file_size


class MediaFile(models.Model):
    def get_upload_path(self, *_args):
        return f"uploads/{self.guid}"

    FILE_STATUSES = (("UPLOAD_COMPLETE",) * 2, ("CONVERTING",) * 2, ("FAILED",) * 2, ("DONE",) * 2)
    OUTPUT_FORMAT_CHOICES = (("mp4", "MP4"), ("mov", "MOV"), ("mpg", "MPG"), ("avi", "AVI"))

    guid = models.UUIDField(default=uuid4, unique=True, primary_key=True)
    input_file = models.FileField(upload_to=get_upload_path, validators=[validate_file_size, validate_file_name])
    output_file = models.FileField(null=True)
    output_format = models.CharField(choices=OUTPUT_FORMAT_CHOICES, max_length=3)
    status = models.CharField(choices=FILE_STATUSES, max_length=16, default="UPLOAD_COMPLETE")
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    updated_time = models.DateTimeField(auto_now=True)
