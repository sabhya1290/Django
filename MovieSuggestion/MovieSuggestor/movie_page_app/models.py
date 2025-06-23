from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.
class Movies(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    released_year = models.IntegerField(default=datetime.datetime.now().year) 
    tags = TaggableManager()
    description = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],default=3)
    video_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name
