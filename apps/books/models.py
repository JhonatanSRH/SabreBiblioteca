from django.db import models
from apps.user.models import User


class Library(models.Model):
    """Modelo Biblioteca"""
    id = models.AutoField(primary_key=True)
    user_register = models.ManyToManyField(User, related_name="library_set", related_query_name="library",)
    
    def add_book(self, book: object): 
        """Añade un libro a la lista de libros de la biblioteca."""
        book.library = self
        book.save()
        
    def register_user(self, user: object): 
        """Añade un usuario a la lista de usuarios de la biblioteca."""
        self.user_register.add(user)
        self.save()
        
    def lend_book(self, title: str, user_borrow: object): 
        """Permite a un usuario prestar un libro disponible por su título. Retorna True si se pudo prestar el libro, y False en caso contrario."""
        book = Book.objects.get(title=title)
        if user_borrow not in self.user_register.all():
            self.register_user(user_borrow)
        if book.available:
            return user_borrow.borrow(book)
        return False
        
    def get_back_book(self, title: str, user_borrow: object): 
        """Permite a un usuario devolver un libro prestado por su título. Retorna True si se pudo devolver el libro, y False en caso contrario."""
        book = Book.objects.get(title=title)
        if book.user_borrow == user_borrow and not book.available:
            return user_borrow.get_back(book)
        return False

class Book(models.Model):
    """Modelo Libro"""
    title = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    available = models.BooleanField(default=0)
    user_borrow = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, null=True)

    def lend(self) -> bool:
        """Marca el libro como no disponible si está disponible, y retorna True; de lo contrario, retorna False.
        
        Args:

        Returns:
            bool: disponibilidad del libro
        """
        if self.available:
            self.available = False
        return self.available
    
    def get_back(self):
        """Marca el libro como disponible.
        
        Args:

        Returns:
            bool: disponibilidad del libro
        """
        self.available = True
        self.user_borrow = None

    def __str__(self):
        return '%d: %s' % (self.id, self.title)
