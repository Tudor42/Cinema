from django.db.models.fields import TextField
from .serializers import FilmSerializer,\
                         RezervareSerializer
from .models import Film, Rezervare
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, schema
from django.db.models import Count, Q
from django.db.models.functions import Cast
import random
import string
import math
from cinema.schemas import Schemas, FilmListAutoSchema, \
                           FilmDetailAutoSchema


@api_view(['POST'])
@schema(Schemas.generate_random)
def films_generate_random(request: Request, n) -> Response:
    """
    post:
        Takes an integer var from path variable var and generates var
        random entities
    """
    if request.method == 'POST':
        objs = []  # list with objects
        for i in range(int(n)):
            obj = Film(
                titlu=''.join([random.choice(string.ascii_letters)
                               for i in range(10)]),
                an_aparitie=random.randint(1878, 2022),
                pret=random.randint(1, 300),
                in_program=random.choice([True, False]),
            )
            objs.append(obj)
        Film.objects.bulk_create(objs)

        num = Film.objects.count()  # number of elems in the database
        data = Film.objects.all()[num-int(n):]  # get last n elems

        serializer = FilmSerializer(data=data,
                                    many=True)
        serializer.is_valid()
        # we send serializer data with all objects created so the frontend
        # can use it to undo
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def films_list_descending(request: Request, page) -> Response:
    """
    get:
        Gets all films in a descending order by number of bookings
        to the film
    """
    if request.method == 'GET':
        try:
            page = int(page)
        except Exception:
            page = None
        maxpage = math.ceil(Film.objects.all().count()/10)
        if maxpage <= page:
            page = maxpage - 1
        if page < 0:
            page = 0
        if page is not None:
            data = Film.objects.annotate(Count('rezervare')).\
                    order_by("-rezervare__count")[page*10: page*10+10]
        else:
            data = Film.objects.annotate(Count('rezervare')).\
                    order_by("-rezervare__count")
        serializer = FilmSerializer(data, context={'request': request},
                                    many=True)
        return Response(
            {
                'data': serializer.data,
                'page': page,
                'maxpage': maxpage
            }
        )


@api_view(['POST'])
@schema(Schemas.film_list_proprety)
# TODO extend the view to more than one property
def films_list_property(request: Request) -> Response:
    """
    post:
        Takes in a variable in_program(can be True or False)
        and returns films with that proprety
    """
    if request.method == 'POST':
        try:
            text = request.data['search'].strip().split()
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for prop in request.data:
            if prop == "in_program":
                films = \
                    Film.objects.filter(in_program=request.data[prop])
        films = films.annotate(
            id_as_str=Cast('id', TextField()),
            an_as_str=Cast('an_aparitie', TextField()),
            pret_as_str=Cast('pret', TextField()),
        )
        for t in text:
            t = t.lower()
            if t in "true":
                films = films.filter(
                    Q(id_as_str__icontains=t) |
                    Q(titlu__icontains=t) |
                    Q(an_as_str__icontains=t) |
                    Q(pret_as_str__icontains=t) |
                    Q(in_program=True)
                )
            elif t in "false":
                films = films.filter(
                    Q(id_as_str__icontains=t) |
                    Q(titlu__icontains=t) |
                    Q(an_as_str__icontains=t) |
                    Q(pret_as_str__icontains=t) |
                    Q(in_program=False)
                )
            else:
                films = films.filter(
                    Q(id_as_str__icontains=t) |
                    Q(titlu__icontains=t) |
                    Q(an_as_str__icontains=t) |
                    Q(pret_as_str__icontains=t)
                )
        films = films[:10]
        serializer = FilmSerializer(films, context={'request': request},
                                    many=True)
        # data = Film.objects.filter(in_program=property)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@schema(FilmListAutoSchema())
def films_list(request: Request, page=None) -> Response:
    """
    get:
        Get all the films in database

    post:
        Create a new film entity

    """
    if request.method == 'GET':
        try:
            page = int(page)
        except Exception:
            page = None
        maxpage = math.ceil(Film.objects.all().count()/10)
        if maxpage <= page:
            page = maxpage - 1
        if page < 0:
            page = 0
        if page is not None:
            data = Film.objects.all()[page*10: page*10+10]
        else:
            data = Film.objects.all()
        serializer = FilmSerializer(data, context={'request': request},
                                    many=True)

        return Response(
            {
                'data': serializer.data,
                'page': page,
                'maxpage': maxpage
            }
        )

    elif request.method == 'POST':
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id=request.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE', 'GET'])  # GET to get a movie by id
@schema(FilmDetailAutoSchema())
def film_detail(request: Request, id) -> Response:
    """
    put:
        Modify object with id given in the url
    delete:
        Delete object with id given in the url
    get:
        Get object with id given in the url
    """
    try:
        film = Film.objects.get(id=id)
    except Film.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        prevstate = FilmSerializer(film).data  # il will be send back to
        # frontend for undo-redo
        serializer = FilmSerializer(film, data=request.data,
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"prevdata": prevstate,
                    "postdata": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # we do this extra steps because
        # delete makes id data null
        # but we'll need it for undo-redo
        data = FilmSerializer(film).data
        rezervari = Rezervare.objects.filter(id_film=data['id'])
        rezervari = RezervareSerializer(rezervari, many=True).data
        # this bookings will be deleted because of on_delete=CASCADE
        # so we should save their state for undo-redo and send it to
        # frontend
        film.delete()
        return Response([data, rezervari], status=status.HTTP_200_OK)

    elif request.method == 'GET':
        serializer = FilmSerializer(film)
        return Response(serializer.data)


@api_view(['PUT'])
def full_text_films(request: Request) -> Response:
    """
    put:
        Uses a string passed in the query as text and do a full search in films
    """
    if request.method == 'PUT':
        try:
            text = request.data['text']
            text = text.strip().lower().split()
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            first_10 = request.data['first_10']
        except KeyError:
            first_10 = False
        try:
            page = int(request.data['page'])
        except KeyError:
            page = None
        if first_10 and text == []:
            return Response([])

        films = Film.objects.all().annotate(
            id_as_str=Cast('id', TextField()),
            an_as_str=Cast('an_aparitie', TextField()),
            pret_as_str=Cast('pret', TextField()),
        )
        for t in text:
            if t in "true":
                films = films.filter(
                    Q(id_as_str__icontains=t) |
                    Q(titlu__icontains=t) |
                    Q(an_as_str__icontains=t) |
                    Q(pret_as_str__icontains=t) |
                    Q(in_program=True)
                )
            elif t in "false":
                films = films.filter(
                    Q(id_as_str__icontains=t) |
                    Q(titlu__icontains=t) |
                    Q(an_as_str__icontains=t) |
                    Q(pret_as_str__icontains=t) |
                    Q(in_program=False)
                )
            else:
                films = films.filter(
                    Q(id_as_str__icontains=t) |
                    Q(titlu__icontains=t) |
                    Q(an_as_str__icontains=t) |
                    Q(pret_as_str__icontains=t)
                )
        maxpage = math.ceil(films.count()/10)
        if maxpage <= page:
            page = maxpage - 1
        if page < 0:
            page = 0
        films = films[10*page:10*page+10]
        serializer_f = FilmSerializer(films, many=True).data
        return Response(
            {
                'data': serializer_f,
                'page': page,
                'maxpage': maxpage
            },
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def films_multiple_add(request):
    """
    post:
        Uses the list of films passed in the query and add them all to
        the database
    """
    if request.method == 'POST':
        objs = []
        for entity in request.data:
            objs.append(Film(
                id=entity['id'],
                titlu=entity['titlu'],
                an_aparitie=entity['an_aparitie'],
                pret=entity['pret'],
                in_program=entity['in_program']
            ))
        Film.objects.bulk_create(objs)
        return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
def films_multiple_delete(request):
    """
    put:
        Uses list of films passed in the query and uses their id to delete them
    """
    if request.method == 'PUT':
        ids = [entity['id'] for entity in request.data]
        for i in range(0, len(ids), 10000):
            Film.objects.filter(id__in=ids[i: i+10000]).delete()
        Film.objects.filter(id__in=ids[i:]).delete()
        return Response(status=status.HTTP_200_OK)
