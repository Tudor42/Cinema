import coreapi
import coreschema
from rest_framework import schemas


class Schemas:
    generate_random = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="var",
                required=True,
                location="path",
                schema=coreschema.String(title="var", description="Number of"
                                         " entities to create"),
            )
        ]
    )

    film_list_proprety = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="in_program",
                required=False,
                location="query",
                schema=coreschema.String(title="var", description="Can be true"
                                         " or false"),
            ),
            coreapi.Field(
                name="search",
                required=False,
                location="query",
                schema=coreschema.String(title="var", description="A string"
                                         " that with whom we perform a"
                                         " fullsearch on film "
                                         " with propreties given"
                                         " and return first"
                                         " 10 films that corespond to query"),
            )
        ]
    )

    card_add_points = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="n",
                required=True,
                location="query",
                schema=coreschema.String(title="n",
                                         description="Number of points"),
            ),
            coreapi.Field(
                name="date_gte",
                required=True,
                location="query",
                schema=coreschema.String(title="date_gte",
                                         description="Lower bound date"),
            ),
            coreapi.Field(
                name="date_lte",
                required=True,
                location="query",
                schema=coreschema.String(title="date_lte",
                                         description="Upper bound date"),
            )
        ]
    )

    bookings_filter = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="var",
                required=True,
                location="path",
                schema=coreschema.String(title="var",
                                         description="1-Delete between dates\n"
                                                     "2-Filter between hours"),
            ),
            coreapi.Field(
                name="date_gte",
                required=False,
                location="query",
                schema=coreschema.String(title="date_gte",
                                         description="Lower bound date"),
            ),
            coreapi.Field(
                name="date_lte",
                required=False,
                location="query",
                schema=coreschema.String(title="date_lte",
                                         description="Upper bound date"),
            ),
            coreapi.Field(
                name="time_gte",
                required=False,
                location="query",
                schema=coreschema.String(title="time_gte",
                                         description="Lower bound time"),
            ),
            coreapi.Field(
                name="time_lte",
                required=False,
                location="query",
                schema=coreschema.String(title="time_lte",
                                         description="Upper bound time"),
            )
        ]
    )

    full_search_clients = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="text",
                required=True,
                location="query",
                schema=coreschema.String(title="text",
                                         description="Text searched"),
            ),
            coreapi.Field(
                name="first_10",
                required=False,
                location="query",
                schema=coreschema.String(title="first_10",
                                         description="Return only first 10"
                                         " bookings"
                                         "coresponding to the query"),
            )
        ]
    )


class FilmListAutoSchema(schemas.AutoSchema):
    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "get":
            custom_fields = []
        if method.lower() == "post":
            custom_fields = \
                [coreapi.Field(
                    name="id",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="id",
                                             description="ID of the film added"
                                                         " if None id is"
                                                         " generated automati"
                                                         "cally")),
                 coreapi.Field(
                    name="titlu",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="titlu",
                                             description="Film title")),
                 coreapi.Field(
                    name="an_aparitie",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="an_aparitie",
                                             description="Year of release")),
                 coreapi.Field(
                    name="pret",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="pret",
                                             description="Ticket price")),
                 coreapi.Field(
                    name="in_program",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="in_program",
                                             description="Is movie"
                                                         " in program"))]
        return custom_fields


class FilmDetailAutoSchema(schemas.AutoSchema):
    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "get":
            custom_fields = \
                [coreapi.Field(
                    name="var",
                    required=True,
                    location="path",
                    schema=coreschema.String(title="var",
                                             description="ID of film"
                                                         " to get"))]
        if method.lower() == "delete":
            custom_fields = \
                [coreapi.Field(
                    name="var",
                    required=True,
                    location="path",
                    schema=coreschema.String(title="var",
                                             description="ID of film"
                                                         " to delete"))]
        if method.lower() == "put":
            custom_fields = \
                [coreapi.Field(
                    name="var",
                    required=True,
                    location="path",
                    schema=coreschema.String(title="var",
                                             description="ID of film"
                                                         " to modify")),
                 coreapi.Field(
                    name="titlu",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="titlu",
                                             description="Film title")),
                 coreapi.Field(
                    name="an_aparitie",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="an_aparitie",
                                             description="Year of release")),
                 coreapi.Field(
                    name="pret",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="pret",
                                             description="Ticket price")),
                 coreapi.Field(
                    name="in_program",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="in_program",
                                             description="Is movie in program")
                 )]
        return self._manual_fields + custom_fields


class CardListAutoSchema(schemas.AutoSchema):
    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "get":
            custom_fields = []
        if method.lower() == "post":
            custom_fields = \
                [coreapi.Field(
                    name="id",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="id",
                                             description="ID of the client "
                                                         "added"
                                                         " if None id is"
                                                         " generated automati"
                                                         "cally")),
                 coreapi.Field(
                    name="nume",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="nume",
                                             description="Client name")),
                 coreapi.Field(
                    name="prenume",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="prenume",
                                             description="Client first name")),
                 coreapi.Field(
                    name="CNP",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="CNP",
                                             description="Identity number")),
                 coreapi.Field(
                    name="data_inregistrarii",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="data_inregistrarii",
                                             description="Date of "
                                             "registration")),
                 coreapi.Field(
                    name="data_nasterii",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="data_nasterii",
                                             description="Date of "
                                             "birth")),
                 coreapi.Field(
                    name="puncte",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="puncte",
                                             description="Number of points")
                )]
        return custom_fields


class CardDetailAutoSchema(schemas.AutoSchema):
    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "delete":
            custom_fields = \
                [coreapi.Field(
                    name="var",
                    required=True,
                    location="path",
                    schema=coreschema.String(title="var",
                                             description="ID of client"
                                                         " to delete"))]
        if method.lower() == "put":
            custom_fields = \
                [coreapi.Field(
                    name="var",
                    required=True,
                    location="path",
                    schema=coreschema.String(title="var",
                                             description="ID of client"
                                                         " to modify")),
                 coreapi.Field(
                    name="nume",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="nume",
                                             description="Client name")),
                 coreapi.Field(
                    name="prenume",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="prenume",
                                             description="Client first name")),
                 coreapi.Field(
                    name="CNP",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="CNP",
                                             description="Identity number")),
                 coreapi.Field(
                    name="data_inregistrarii",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="data_inregistrarii",
                                             description="Date of "
                                             "registration")),
                 coreapi.Field(
                    name="data_nasterii",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="data_nasterii",
                                             description="Date of "
                                             "birth")),
                 coreapi.Field(
                    name="puncte",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="puncte",
                                             description="Number of points")
                )]
        return self._manual_fields + custom_fields


class BookingListAutoSchema(schemas.AutoSchema):
    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "get":
            custom_fields = []
        if method.lower() == "post":
            custom_fields = \
                [coreapi.Field(
                    name="id",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="id",
                                             description="ID of the booking "
                                                         "added"
                                                         " if None id is"
                                                         " generated automati"
                                                         "cally")),
                 coreapi.Field(
                    name="id_film",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="id_film",
                                             description="Film id")),
                 coreapi.Field(
                    name="id_card_client",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="id_card_client",
                                             description="Client id")),
                 coreapi.Field(
                    name="data",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="data",
                                             description="Date")),
                 coreapi.Field(
                    name="ora",
                    required=True,
                    location="query",
                    schema=coreschema.String(title="ora",
                                             description="Hour"))]
        return custom_fields


class BookingDetailAutoSchema(schemas.AutoSchema):
    def get_manual_fields(self, path, method):
        custom_fields = []
        if method.lower() == "delete":
            custom_fields = \
                [coreapi.Field(
                    name="var",
                    required=True,
                    location="path",
                    schema=coreschema.String(title="var",
                                             description="ID of booking"
                                                         " to delete"))]
        if method.lower() == "put":
            custom_fields = \
                [coreapi.Field(
                    name="var",
                    required=True,
                    location="path",
                    schema=coreschema.String(title="var",
                                             description="ID of booking"
                                                         " to modify")),
                 coreapi.Field(
                    name="id_film",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="id_film",
                                             description="Film id")),
                 coreapi.Field(
                    name="id_card_client",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="id_card_client",
                                             description="Client id")),
                 coreapi.Field(
                    name="data",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="data",
                                             description="Date")),
                 coreapi.Field(
                    name="ora",
                    required=False,
                    location="query",
                    schema=coreschema.String(title="ora",
                                             description="Hour"))]
        return self._manual_fields + custom_fields
