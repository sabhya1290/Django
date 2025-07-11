from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only PDF, DOC, and DOCX files are allowed.')


# Create your models here.
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/', validators=[validate_file_extension])
    subject = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title', 'file'], name='unique_user_title_file')
        ]
    def __str__(self):
        return self.title


class Category(models.Model):
    year_choices = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ]
    year = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.year)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.year