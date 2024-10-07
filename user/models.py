from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=250)

    def lend(self, book_instance: object) -> bool:
        """Prestar el libro"""
        if self.book_instance.aviable:
            self.book_instance.aviable = False
        return self.book_instance.aviable
    
    def get_back(self, book_instance: object):
        """Devolver el libro"""
        self.book_instance.aviable = True

