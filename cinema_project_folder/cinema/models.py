from django.db import models

# Create your models here.
from django.db import models
from .custom_validators import movie_year, CNP_validate

# Create your models here.


class Film(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    titlu = models.TextField(max_length=256)
    an_aparitie = models.PositiveIntegerField(validators=[movie_year])
    pret = models.PositiveIntegerField()
    in_program = models.BooleanField()

    def delete(self, *args, **kwargs):
        """
        This method makes sure that in a cascade delete client that
            has a booking to the film is taken the points for that film
        """
        for rezervari in Rezervare.objects.filter(id_film=self.id):
            rezervari.delete()
        super().delete(*args, **kwargs)


class CardClient(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    nume = models.TextField()
    prenume = models.TextField()
    CNP = models.TextField(unique=True, max_length=13,
                           validators=[CNP_validate])
    data_nasterii = models.DateField(auto_now=False, auto_now_add=False)
    data_inregistrarii = models.DateField(auto_now=False, auto_now_add=False)
    puncte = models.IntegerField()


class Rezervare(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    id_film = models.ForeignKey(Film, on_delete=models.CASCADE,
                                limit_choices_to={'in_program': True})
    id_card_client = models.ForeignKey(CardClient, on_delete=models.SET_NULL,
                                       blank=True, null=True)
    data = models.DateField(auto_now=False, auto_now_add=False)
    ora = models.TimeField(auto_now=False, auto_now_add=False)

    def save(self, *args, **kwargs):
        """
        Adds 10% from movie price to client's points
        """
        try:
            rezervare = Rezervare.objects.get(id=self.id)
        except Exception:
            rezervare = None

        if rezervare:
            # it means we update
            # we take points from the client card
            print(rezervare.id_card_client, rezervare.id_film)
            if rezervare.id_card_client:
                card = CardClient.objects.filter(id=rezervare.
                                                 id_card_client.id)
                puncte_card = card[0].puncte
                puncte_card -= (rezervare.id_film.pret//10)
                card.update(puncte=puncte_card)

        # in every case we are adding
        # points to the card to whom the booking
        # was made for
        super().save(*args, **kwargs)
        film = Film.objects.filter(id=self.id_film.id)[0]
        if self.id_card_client:
            card = CardClient.objects.filter(id=self.id_card_client.id)
            puncte_card = card[0].puncte
            puncte_card += (film.pret//10)
            card.update(puncte=puncte_card)

    def delete(self, *args, **kwargs):
        """
        Takes back 10% from movie price from the client
        """
        film = Film.objects.filter(id=self.id_film.id)[0]
        if self.id_card_client:
            card = CardClient.objects.filter(id=self.id_card_client.id)
            puncte_card = card[0].puncte
            puncte_card -= (film.pret//10)
            card.update(puncte=puncte_card)
        super().delete(*args, **kwargs)
