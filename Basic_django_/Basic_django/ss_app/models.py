from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class ChaiVariety(models.Model):
    chai_type_choice=[
        ('PL','Plain'),
        ('GN','Ginger'),
        ('MS','Masala'),
        ('KL','Kiwi'),
        ('EL','Elaichi'),
    ]
    name= models.CharField(max_length=100)
    image=models.ImageField(upload_to="chais/")
    date_added= models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices= chai_type_choice)
    description= models.TextField(default='')

    def __str__(self):
        return self.name
    

#One to Many

class ChaiReview(models.Model):
    chai = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE , related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{User.username} review for {self.chai.name}"
    
#Many to Many

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    chai_varieties = models.ManyToManyField(ChaiVariety, related_name='stores')

    def __str__(self):
        return self.name
    
#One to One

class ChaiCertificates(models.Model):
    chai = models.OneToOneField(ChaiVariety, on_delete=models.CASCADE , related_name='certificate')
    certificate_number = models.CharField(max_length=100)
    issued_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f'certificate for {self.chai.name}'
    
    