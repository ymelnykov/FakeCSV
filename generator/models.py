from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

# Create your models here.

class User(AbstractUser):

    def __str__(self):
        return self.username


class Schema(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)
    DELIMITER_CHOICES = [
        (',', 'Comma (,)'),
        (';', 'Semicolon (;)'),
        (' ', 'Space ( )'),
        ('|', 'Pipe (|)'),
    ]
    delimiter = models.CharField(max_length=2, choices=DELIMITER_CHOICES, default=',', verbose_name='Column separator')
    CHARACTER_CHOICES = [
        ("'", "Single-quote (')"),
        ('"', 'Double-quote (")'),
    ]
    character = models.CharField(max_length=1, choices=CHARACTER_CHOICES, default='"', verbose_name='String character')

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=128, verbose_name='Column name')
    owner = models.ForeignKey(Schema, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        ('name', 'Full name'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('domain_name', 'Domain name'),
        ('phone_number', 'Phone number'),
        ('company', 'Company name'),
        ('paragraph', 'Text'), 
        ('pyint', 'Integer'),
        ('address', 'Address'),
        ('date', 'Date'),
    ]
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    start = models.IntegerField(default=0, verbose_name='From')
    end = models.IntegerField(default=0, verbose_name='To')
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
    
    
class DataSet(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='csv')

    def __str__(self):
        return self.name
    
    @property
    def get_file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url





        