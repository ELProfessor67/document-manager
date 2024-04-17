from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.text import slugify


def user_directory_path(instance, filename):
    # Split the filename and its extension
    base_filename, extension = os.path.splitext(filename)
    # Generate a slugified version of the base filename
    sanitized_filename = slugify(base_filename)
    # Append the extension back
    sanitized_filename_with_extension = f"{sanitized_filename}{extension}"
    # Construct the upload path
    return f"static/documents/{instance.user.username}-{instance.document.id}/{sanitized_filename_with_extension}"


# Create your views here.
class Document(models.Model):
    document_name = models.CharField(max_length=100)
    about_description = models.TextField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.document_name


class DocumentFile(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path) 