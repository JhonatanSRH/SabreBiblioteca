from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.books.models import Book, Library


User = get_user_model()

class LibraryTestCase(TestCase):
    """Library Test Case."""

    def setUp(self):
        try:
            self.client = Client()
            self.user = User.objects.create_user(
                username='prueba@prueba.com',
                email='prueba@prueba.com',
                password='admin1234*',
                name='sr prueba'
            )
            self.library = Library.objects.create()
            self.book = Book.objects.create(
                title="1984",
                autor="George Orwell",
                available=1
            )
        except Exception as error:
            print('error on setup')
            print(str(error))

    def test_add_book(self):
        """Agregar Libro: Verifica que un libro se pueda agregar a la biblioteca."""
        data = {
            'book': self.book.pk
        }
        response = self.client.post(f'/apps/library/{self.library.pk}/add_book/',
                                    data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get('result'))
    
    def test_register_user(self):
        """Registrar Usuario: Verifica que un usuario se pueda registrar en la biblioteca."""
        data = {
            'user': self.user.pk
        }
        response = self.client.post(f'/apps/library/{self.library.pk}/register_user/',
                                    data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get('result'))
    
    def test_borrow_book(self):
        """Prestar Libro Disponible: Verifica que un libro disponible se pueda prestar a un usuario."""
        self.book.library = self.library
        self.book.save()
        data = {
            'title': self.book.title,
            'user_borrow': self.user.pk
        }
        response = self.client.post(f'/apps/library/{self.library.pk}/borrow_book/',
                                    data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get('result'))
    
    def test_borrow_book_fail(self):
        """Prestar Libro No Disponible: Verifica que un libro no disponible no se pueda prestar."""
        book_2 = Book.objects.create(
            title="100 años de soledad",
            autor="Miguel de Cervantes",
            available=0,
            library=self.library,
            user_borrow=self.user
        )
        data = {
            'title': book_2.title,
            'user_borrow': self.user.pk
        }
        response = self.client.post(f'/apps/library/{self.library.pk}/borrow_book/',
                                    data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data.get('result'))
    
    def test_get_back_book(self):
        """Devolver Libro Prestado: Verifica que un libro prestado se pueda devolver."""
        book_2 = Book.objects.create(
            title="100 años de soledad",
            autor="Miguel de Cervantes",
            available=0,
            library=self.library,
            user_borrow=self.user
        )
        data = {
            'title': book_2.title,
            'user_borrow': self.user.pk
        }
        response = self.client.post(f'/apps/library/{self.library.pk}/get_back_book/',
                                    data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get('result'))

    def test_get_back_book_fail(self):
        """Devolver Libro No Prestado: Verifica que un libro que no ha sido prestado no se pueda devolver."""
        book_3 = Book.objects.create(
            title="Harry Potter",
            autor="JK Rowling",
            available=1,
            library=self.library
        )
        data = {
            'title': book_3.title,
            'user_borrow': self.user.pk
        }
        response = self.client.post(f'/apps/library/{self.library.pk}/get_back_book/',
                                    data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data.get('result'))
