from django.urls import path, re_path
import cinema.views as v
import cinema.views_bookings as vb
import cinema.views_cards as vc
import cinema.views_films as vf
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('docs/', include_docs_urls(title='Cinema database API')),
    path('', v.index),
    path('films/', v.index),
    path('clients/', v.index),
    path('bookings/', v.index),
    path('full_text/', v.index),
    # Films api
    re_path(r'^api/films/$', vf.films_list),
    re_path(r'^api/films/([0-9]+)$', vf.film_detail),
    re_path(r'^api/films/page/([0-9]+)$', vf.films_list),
    re_path(r'^api/films/descending/([0-9]+)$', vf.films_list_descending),
    re_path(r'^api/films/descending/$', vf.films_list_descending),
    re_path(r'^api/films/generate_random/([0-9]+)$', vf.films_generate_random),
    re_path(r'^api/films/property/$', vf.films_list_property),
    re_path(r'^api/films_madd/$', vf.films_multiple_add),
    re_path(r'^api/films_mdelete/$', vf.films_multiple_delete),
    # Cards api
    re_path(r'^api/cards/$', vc.cards_list),
    re_path(r'^api/cards/page/([0-9]+)$', vc.cards_list),
    re_path(r'^api/cards/ascending/([0-9]+)$', vc.cards_list_ascending),
    re_path(r'^api/cards/ascending/$', vc.cards_list_ascending),
    re_path(r'^api/cards/([0-9]+)$', vc.card_detail),
    re_path(r'^api/cards/add_points/$', vc.card_add_points),
    re_path(r'^api/cards_mupdate/$', vc.cards_multiple_update),
    # Bookings api
    re_path(r'^api/bookings/$', vb.bookings_list),
    re_path(r'^api/bookings/page/([0-9]+)$', vb.bookings_list),
    re_path(r'^api/bookings/([0-9]+)$', vb.booking_detail),
    re_path(r'^api/bookings_filter/([0-2])$', vb.bookings_filter),
    re_path(r'^api/bookings_madd/$', vb.bookings_multiple_add),
    re_path(r'^api/bookings_mdelete/$', vb.bookings_multiple_delete),
    # Full text search api
    re_path(r'^api/full_text_films/$', vf.full_text_films),
    re_path(r'^api/full_text_cards/$', vc.full_text_cards),
]
