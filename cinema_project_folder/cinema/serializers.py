from rest_framework import serializers
from .models import Film, CardClient, Rezervare


class FilmSerializer(serializers.ModelSerializer):
    str_reprezentation = serializers.SerializerMethodField()
    num_of_bookings = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ['id', 'titlu', 'an_aparitie', 'pret', 'in_program',
                  'str_reprezentation', 'num_of_bookings']

    def get_num_of_bookings(self, obj: Film) -> str:
        return Rezervare.objects.filter(id_film=obj.id).count()

    def get_str_reprezentation(self, obj: Film) -> str:
        return str(obj.titlu)+' ('+str(obj.an_aparitie) + ') ['\
               + str(obj.id)+']'


class CardClientSerializer(serializers.ModelSerializer):
    str_reprezentation = serializers.SerializerMethodField()

    class Meta:
        model = CardClient
        fields = ['id', 'nume', 'prenume',
                  'CNP', 'data_nasterii', 'data_inregistrarii', 'puncte',
                  'str_reprezentation']
        extra_kwargs = {"data_nasterii": {'error_messages': {
                            "invalid": "Date has wrong format. Use one of"
                            " these formats instead: DD.MM.YYYY.\n"
                            "Make sure day, month, and year have valid range"
                            " values"
                        }},
                        "data_inregistrarii": {'error_messages': {
                            "invalid": "Date has wrong format. Use one of"
                            " these formats instead: DD.MM.YYYY.\n"
                            "Make sure day, month, and year have valid range"
                            " values"
                        }}
                        }

    def get_str_reprezentation(self, obj: CardClient) -> str:
        return str(obj.nume)+' '+str(obj.prenume) + ' ['\
               + str(obj.id)+']'


class RezervareSerializer(serializers.ModelSerializer):
    str_film = serializers.SerializerMethodField()
    str_client = serializers.SerializerMethodField()

    class Meta:
        model = Rezervare
        fields = ['id', 'id_film', 'id_card_client',
                  'data', 'ora', 'str_film', 'str_client']
        extra_kwargs = {"id_film": {'error_messages': {"does_not_exist": "Movi"
                                                       "e with this ID doesnt"
                                                       " exist"}},
                        "id_card_client": {'error_messages': {"does_not_exist":
                                                              "Card with this "
                                                              "ID doesnt exist"
                                                              }
                                           },
                        "data": {'error_messages': {
                            "invalid": "Date has wrong format. Use one of"
                            " these formats instead: DD.MM.YYYY.\n"
                            "Make sure day, month, and year have valid range"
                            " values"
                        }}
                        }

    def get_str_film(self, obj: Rezervare) -> str:
        ser = FilmSerializer(obj.id_film)
        return ser.data['str_reprezentation']

    def get_str_client(self, obj: Rezervare) -> str:
        if obj.id_card_client:
            return CardClientSerializer(obj.id_card_client).\
                data['str_reprezentation']


class ViewFilmSerializer:
    class Meta:
        model = Film
        fields = ['id']


class ViewCardClientSerializer:
    class Meta:
        model = CardClient
        fields = ['id']


class ViewRezervareSerializer:
    class Meta:
        model = Rezervare
        fields = ['id']
