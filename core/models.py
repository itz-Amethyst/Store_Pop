from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint

# Create your models here.
class User(AbstractUser):
  email = models.EmailField(unique=True)

  def save(self, *args, **kwargs):
    if not self.first_name and self.is_staff:
      unique_number = randint(1000, 9999)
      self.first_name = f"admin{unique_number}"

    super().save(*args, **kwargs)