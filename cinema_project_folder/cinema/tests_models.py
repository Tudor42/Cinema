from django.test import TestCase
from .models import Film, CardClient, Rezervare
from datetime import date, time
# Create your tests here.


class BaseModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.film1 = Film(
            id=1,
            titlu="WALL-E",
            an_aparitie=2008,
            pret=20,
            in_program=True,
        )
        cls.film1.save()
        cls.film2 = Film(
            id=2,
            titlu="Django Unchained",
            an_aparitie=2012,
            pret=40,
            in_program=True,
        )
        cls.film2.save()
        cls.film3 = Film(
            id=3,
            titlu="The Shawshank Redemption",
            an_aparitie=1994,
            pret=50,
            in_program=False,
        )
        cls.film3.save()
        cls.cardClient1 = CardClient(
            id=1,
            nume="Caan",
            prenume="James",
            CNP="2313451263421",
            data_nasterii=date(2000, 12, 2),
            data_inregistrarii=date(2021, 2, 13),
            puncte=0,
        )
        cls.cardClient1.save()
        cls.cardClient2 = CardClient(
            id=2,
            nume="Feynman",
            prenume="Richard",
            CNP="9823412345234",
            data_nasterii=date(1998, 3, 4),
            data_inregistrarii=date(2012, 4, 5),
            puncte=15,
        )
        cls.cardClient2.save()
        cls.rezervare1 = Rezervare(
            id=1,
            id_film=cls.film1,
            id_card_client=cls.cardClient2,
            data=date(2022, 3, 12),
            ora=time(12, 00),
        )
        cls.rezervare1.save()
        cls.rezervare2 = Rezervare(
            id=2,
            id_film=cls.film2,
            data=date(2023, 4, 1),
            ora=time(9, 15),
        )
        cls.rezervare2.save()


class FilmModelTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEquals(self.film2.titlu, "Django Unchained")
        self.assertEquals(self.film3.in_program, False)
        self.assertEquals(self.film1.id, 1)


class CardClientModelTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEquals(self.cardClient1.nume, "Caan")
        self.assertEquals(self.cardClient2.prenume, "Richard")
        self.assertEquals(self.cardClient2.data_inregistrarii,
                          date(2012, 4, 5))
        self.assertEqual(CardClient.objects.
                         filter(id=self.cardClient2.id)[0].puncte,
                         17)


class RezervareModelTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEquals(self.rezervare2.id_film, self.film2)
        self.assertEquals(self.rezervare1.ora, time(12, 00))
        self.assertEquals(self.rezervare1.id, 1)
