from django.db import models

#from user.models import User


class Library(models.Model):
    user_register = models.ForeignKey(User, on_delete=models.CASCADE)
    
    

class Book(models.Model):
    title = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    aviable = models.BooleanField(default=0)
    user_borrow = models.ForeignKey(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    