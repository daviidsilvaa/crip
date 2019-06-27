from django.db import models
from django.conf import settings
# cria os modelos

class Document(models.Model):
    docfile = models.FileField(upload_to=settings.MEDIA_ROOT)
