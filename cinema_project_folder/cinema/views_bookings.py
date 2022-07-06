from .serializers import RezervareSerializer
from .models import CardClient, Film, Rezervare
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, schema
import datetime
from cinema.schemas import Schemas, BookingListAutoSchema, \
                           BookingDetailAutoSchema
import math


@api_view(['GET', 'POST'])
@schema(BookingListAutoSchema())
def bookings_list(request: Request, page=None) -> Response:
    """
    get:
        Get all bookings

    post:
        Create a new booking
    """
    if request.method == 'GET':
        try:
            page = int(page)
        except Exception:
            page = None
        maxpage = math.ceil(Rezervare.objects.all().count()/10)
        if maxpage <= page:
            page = maxpage - 1
        if page < 0:
            page = 0
        if page is not None:
            data = Rezervare.objects.all()[page*10: page*10+10]
        else:
            data = Rezervare.objects.all()
        serializer = RezervareSerializer(data, context={'request': request},
                                         many=True)
        return Response(
            {
                'data': serializer.data,
                'page': page,
                'maxpage': maxpage
            }
        )

    elif request.method == 'POST':
        serializer = RezervareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id=request.data['id'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@schema(Schemas.bookings_filter)
def bookings_filter(request: Request, n) -> Response:
    """
    put:
        Filter or delete bookings
    """
    if request.method == 'PUT':
        if n == '1':  # delete by date
            try:
                d1 = request.data['date_gte']
                d2 = request.data['date_lte']
                s1 = d1.split('-')
                s2 = d2.split('-')
                datetime.date(int(s1[0]), int(s1[1]), int(s1[2]))
                datetime.date(int(s2[0]), int(s2[1]), int(s2[2]))
            except (ValueError, KeyError, IndexError, Exception):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            objs = Rezervare.objects.filter(data__gte=d1,
                                            data__lte=d2)
            data = RezervareSerializer(objs, many=True).data
            objs.delete()
            return Response(data, status=status.HTTP_200_OK)
        elif n == '2':  # filter by time
            try:
                d1 = request.data['time_gte']
                d2 = request.data['time_lte']
                s1 = d1.split(':')
                s2 = d2.split(':')
                datetime.time(int(s1[0]), int(s1[1]))
                datetime.time(int(s2[0]), int(s2[1]))
            except (ValueError, KeyError, IndexError, Exception):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                page = request.data['page']
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            data = Rezervare.objects.filter(ora__gte=request.data['time_gte'],
                                            ora__lte=request.data['time_lte'])
            maxpage = math.ceil(data.count()/10)
            if maxpage <= page:
                page = maxpage - 1
            if page < 0:
                page = 0
            data = data[page*10:page*10+10]
            serializer = RezervareSerializer(data=data,
                                             context={'request': request},
                                             many=True)
            serializer.is_valid()
            return Response(
                {
                    'data': serializer.data,
                    'page': page,
                    'maxpage': maxpage
                }
            )


@api_view(['PUT', 'DELETE'])
@schema(BookingDetailAutoSchema())
def booking_detail(request: Request, id) -> Response:
    """
    put:
        Modify an object with given id

    delete:
        Delete an object with given id
    """
    try:
        booking = Rezervare.objects.get(id=id)
    except Rezervare.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = RezervareSerializer(booking, data=request.data,
                                         context={'request': request})
        if serializer.is_valid():
            prevdata = RezervareSerializer(booking).data
            serializer.save()
            return Response(
                {
                    'prevdata': prevdata,
                    'postdata': serializer.data
                },
                status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        data = RezervareSerializer(booking).data
        booking.delete()
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def bookings_multiple_add(request):
    """
    post:
        Uses the list of bookings passed in the query and add them all in
        database
    """
    if request.method == 'POST':
        objs = []
        for entity in request.data:
            try:
                client = \
                    CardClient.objects.get(id=entity['id_card_client'])
            except Exception:
                client = None
            try:
                film = Film.objects.get(id=entity['id_film'])
            except Exception:
                film = None
            objs.append(Rezervare(
                id=entity['id'],
                id_film=film,
                id_card_client=client,
                data=entity['data'],
                ora=entity['ora'],
            ))
        Rezervare.objects.bulk_create(objs)
        return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
def bookings_multiple_delete(request):
    """
    put:
        Uses list of bookings passed in the query and delete bookings
        with respective ids
    """
    if request.method == 'PUT':
        ids = [entity['id'] for entity in request.data]
        for i in range(0, len(ids), 10000):
            Rezervare.objects.filter(id__in=ids[i: i+10000]).delete()
        Rezervare.objects.filter(id__in=ids[i:]).delete()
        return Response(status=status.HTTP_200_OK)
