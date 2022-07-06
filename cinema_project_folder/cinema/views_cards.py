from django.db.models.fields import TextField
from .serializers import CardClientSerializer
from .models import CardClient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, schema
import datetime
import math
from django.db.models.functions import Cast
from django.db.models import Q
from cinema.schemas import Schemas, CardListAutoSchema, \
                           CardDetailAutoSchema


@api_view(['PUT'])
@schema(Schemas.card_add_points)
def card_add_points(request: Request) -> Response:
    """
    put:
        Add points to clients cards with birthdays in a given day interval
    """
    if(request.method == 'PUT'):
        try:
            d1 = request.data['date_gte']
            d2 = request.data['date_lte']
            s1 = d1.split('-')
            s2 = d2.split('-')
            datetime.date(int(s1[0]), int(s1[1]), int(s1[2]))
            datetime.date(int(s2[0]), int(s2[1]), int(s2[2]))
        except (ValueError, KeyError, IndexError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            n = int(request.data['n'])
        except (ValueError, KeyError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if n < 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        objs = CardClient.objects.filter(data_nasterii__gte=d1,
                                         data_nasterii__lte=d2)
        prevdata = CardClientSerializer(objs, many=True).data  # save initial
        # state to send it to the frontend

        for obj in objs:
            obj.puncte += n  # update puncte of objects
        CardClient.objects.bulk_update(objs, ['puncte'])

        objs = CardClient.objects.filter(data_nasterii__gte=d1,  # get updated
                                         data_nasterii__lte=d2)  # objs
        postdata = CardClientSerializer(objs, many=True).data  # serialize objs
        # data to send
        # it back

        return Response(
            {
                'prevdata': prevdata,
                'postdata': postdata
            },
            status=status.HTTP_200_OK)


@api_view(['GET'])
def cards_list_ascending(request: Request, page=None) -> Response:
    """
    get:
        Get cards in an ascending order by number of points
    """
    if(request.method == "GET"):
        try:
            page = int(page)
        except Exception:
            page = None
            print("return all")
        maxpage = math.ceil(CardClient.objects.all().count()/10)
        if maxpage <= page:
            page = maxpage - 1
        if page < 0:
            page = 0
        if page is not None:
            data = CardClient.objects.order_by("-puncte")[page*10: page*10+10]
        else:
            data = CardClient.objects.order_by("-puncte")
        serializer = CardClientSerializer(data, context={'request': request},
                                          many=True)
        return Response(
            {
                'data': serializer.data,
                'page': page,
                'maxpage': maxpage
            }
        )


@api_view(['GET', 'POST'])
@schema(CardListAutoSchema())
def cards_list(request: Request, page=None) -> Response:
    """
    get:
        Get all cards
    post:
        Add a new instance of card
    """
    if request.method == 'GET':
        try:
            page = int(page)
        except Exception:
            page = None
        maxpage = math.ceil(CardClient.objects.all().count()/10)
        if maxpage <= page:
            page = maxpage - 1
        if page < 0:
            page = 0
        if page is not None:
            data = CardClient.objects.all()[page*10: page*10+10]
        else:
            data = CardClient.objects.all()
        serializer = CardClientSerializer(data, context={'request': request},
                                          many=True)
        return Response(
            {
                'data': serializer.data,
                'page': page,
                'maxpage': maxpage
            }
        )

    elif request.method == 'POST':
        serializer = CardClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id=request.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@schema(CardDetailAutoSchema())
def card_detail(request: Request, id) -> Response:
    """
    put:
        Modify object with id given in the url

    delete:
        Delete object with id given in the url
    """
    try:
        card = CardClient.objects.get(id=id)
    except CardClient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        prevdata = CardClientSerializer(card).data  # save initial state
        # to return it
        serializer = CardClientSerializer(card, data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'prevdata': prevdata,
                    'postdata': serializer.data
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        data = CardClientSerializer(card).data
        card.delete()
        return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@schema(Schemas.full_search_clients)
def full_text_cards(request: Request) -> Response:
    """
    put:
        Uses a string passed in the query as text and do a full search in cards
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
            page = request.data['page']
        except KeyError:
            page = None
        cards = CardClient.objects.all().annotate(
            id_as_str=Cast('id', TextField()),
            puncte_as_str=Cast('puncte', TextField()),
            nas_as_str=Cast('data_nasterii', TextField()),
            inr_as_str=Cast('data_inregistrarii', TextField())
        )
        for t in text:
            cards = cards.filter(
                Q(id_as_str__icontains=t) |
                Q(nume__icontains=t) |
                Q(prenume__icontains=t) |
                Q(CNP__icontains=t) |
                Q(nas_as_str__icontains=t) |
                Q(inr_as_str__icontains=t) |
                Q(puncte_as_str__contains=t)
            )

        if first_10:
            cards = cards[:10]
            serializer_c = CardClientSerializer(cards, many=True)
            return Response(
                serializer_c.data,
                status=status.HTTP_200_OK
            )
        else:
            if page is not None:
                maxpage = math.ceil(cards.count()/10)
                if maxpage <= page:
                    page = maxpage - 1
                if page < 0:
                    page = 0
                cards = cards[10*page:10*page+10]
                serializer_c = CardClientSerializer(cards, many=True)

        return Response(
            {
                'data': serializer_c.data,
                'page': page,
                'maxpage': maxpage
            },
            status=status.HTTP_200_OK
        )


@api_view(['PUT'])
def cards_multiple_update(request):
    """
    put:
        Uses list of cards passed in the query and update cards with
        acording ids to a new state from the list
    """
    if request.method == 'PUT':
        objs = []
        for entity in request.data:
            objs.append(CardClient(
                id=entity['id'],
                nume=entity['nume'],
                prenume=entity['prenume'],
                CNP=entity['CNP'],
                data_inregistrarii=entity['data_inregistrarii'],
                data_nasterii=entity['data_nasterii'],
                puncte=entity['puncte']
            ))
        CardClient.objects.bulk_update(objs, fields=['puncte'])
        return Response(status=status.HTTP_200_OK)
