from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=250)

    def borrow(self, book: object) -> bool:
        """Añade el libro a la lista de libros prestados si está disponible, y lo marca como no disponible. 
        Retorna True si se pudo prestar el libro, y False en caso contrario.
        
        Args:
            book (object): instancia libro
        Returns:
            bool: disponibilidad del libro
        """
        if book.available:
            book.user_borrow = self
            book.lend()
            book.save()
            return True
        return False
    
    def get_back(self, book: object):
        """Elimina el libro de la lista de libros prestados y lo marca como disponible. Retorna True si se pudo devolver el libro, y False en caso contrario.
        
        Args:
            book (object): instancia libro
        Returns:
            bool: disponibilidad del libro
        """
        if not book.available:
            book.get_back()
            book.save()
            return True
        return False
