from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    # Web UI Interfaces
    path('', views.list_reservations, name='reservations_list'),
    path('list/', views.list_reservations, name='reservations_list'),
    path('book/', views.book_reservation, name='book_reservation'),
    path('cancel/<int:id>/', views.cancel_reservation, name='cancel_reservation'),

    #  api/v1: FBV
    path('api/v1/', views.reservation_api_list, name='v1_list'),
    path('api/v1/<int:id>/', views.reservation_api_detail, name='v1_detail'),

    # api/v2: CBV APIView
    path('api/v2/', views.ReservationListCBV.as_view(), name='v2_list'),
    path('api/v2/<int:id>/', views.ReservationDetailCBV.as_view(), name='v2_detail'),

    #  api/v3: Mixins
    path('api/v3/', views.ReservationListMixins.as_view(), name='v3_list'),
    path('api/v3/<int:id>/', views.ReservationDetailMixins.as_view(), name='v3_detail'),

    #  api/v4: Generic Views
    path('api/v4/', views.ReservationListGenerics.as_view(), name='v4_list'),
    path('api/v4/<int:id>/', views.ReservationDetailGenerics.as_view(), name='v4_detail'),
]