from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    author = models.CharField(max_length=255)
    genere = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

class Member(AbstractUser):
    phone = models.CharField(max_length=10)
    address = models.TextField()
    email = models.EmailField(unique=True)

    #optinal(overidding it, for make it optional)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
      return "{}".format(self.email)

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        if self.book.available_copies <= 0:
            raise ValidationError(f"No copies of '{self.book.title}' are available.")
        
    def save(self, **kwargs):
        """
         the below condition is to make sure that, it only executes on creation of object(because at the time of creation of object self.pk is None)

         ref: https://docs.djangoproject.com/en/5.1/ref/models/instances/#how-django-knows-to-update-vs-insert
         
        """
        if not self.pk: 
            self.clean()
            self.book.available_copies -= 1
            if self.book.available_copies < 0:
                raise ValidationError(f"Not enough copies available.")
            self.book.save()
        super().save(**kwargs)  