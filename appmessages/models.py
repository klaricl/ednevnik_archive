from django.db import models

# Create your models here.

class ContactMessages(models.Model):
    name = models.CharField(max_length = 40)
    email = models.EmailField(max_length = 40)
    subject = models.CharField(max_length = 100)
    message = models.TextField(max_length = 1000)

    def __str__(self):
        return self.subject
