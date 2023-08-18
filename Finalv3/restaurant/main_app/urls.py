from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path('dishes/', views.dishes, name='dishes'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),

    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('staff_list/', views.staff_list, name='staff_list'),

    path('create_reservation/', views.create_reservation, name='create_reservation'),
    path('cancelled_reservation/', views.cancelled_reservation, name='cancelled_reservation'),
    path('edit_reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('reservations/', views.reservations, name='reservations'),
    path('unactive_reservations/', views.unactive_reservations, name='unactive_reservations'),
    path('finished_reservations/', views.finished_reservations, name='finished_reservations'),

    path('create_news/', views.create_news, name='create_news'),
    path('orders/', views.orders, name='orders'),
]
