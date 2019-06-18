from django.db import models

# cria os modelos

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
