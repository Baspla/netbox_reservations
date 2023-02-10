from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    # Reservation
    path('reservations/', views.ReservationListView.as_view(), name='reservation_list'),
    path('reservations/add/', views.ReservationEditView.as_view(), name='reservation_add'),
    path('reservations/<int:pk>/', views.ReservationView.as_view(), name='reservation'),
    path('reservations/<int:pk>/edit/', views.ReservationEditView.as_view(), name='reservation_edit'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    path('reservations/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='reservation_changelog', kwargs={
        'model': models.Reservation
    }),

    # Claims
    path('claims/', views.ClaimListView.as_view(), name='claim_list'),
    path('claims/add/', views.ClaimEditView.as_view(), name='claim_add'),
    path('claims/<int:pk>/', views.ClaimView.as_view(), name='claim'),
    path('claims/<int:pk>/edit/', views.ClaimEditView.as_view(), name='claim_edit'),
    path('claims/<int:pk>/delete/', views.ClaimDeleteView.as_view(), name='claim_delete'),
    path('claims/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='claim_changelog', kwargs={
        'model': models.Claim
    }),

    # Tag Overview
    path('tags/', views.TagOverviewListView.as_view(), name='tag_overview_list'),

)
