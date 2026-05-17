from django.urls import path
from . import views

app_name = 'guests'

urlpatterns = [ 
    # Web UI 
    path('', views.list_guests, name='guests_list'),
    path('list/', views.list_guests, name='guests_list'),
    path('add/', views.add_guest, name='add_guest'),
    path('edit/<int:id>/', views.edit_guest, name='edit_guest'),
    path('delete/<int:id>/', views.delete_guest, name='delete_guest'),

    #api/v1: FBV
    path('api/v1/', views.guest_api_list, name='v1_list'),
    path('api/v1/<int:id>/', views.guest_api_detail, name='v1_detail'),

    # api/v2 CBV
    path('api/v2/', views.GuestListCBV.as_view(), name='v2_list'),
    path('api/v2/<int:id>/', views.GuestDetailCBV.as_view(), name='v2_detail'),

    # api/v3 Mixins
    path('api/v3/', views.GuestListMixins.as_view(), name='v3_list'),
    path('api/v3/<int:id>/', views.GuestDetailMixins.as_view(), name='v3_detail'),

    # api/v4 Generic Views
    path('api/v4/', views.GuestListGenerics.as_view(), name='v4_list'),
    path('api/v4/<int:id>/', views.GuestDetailGenerics.as_view(), name='v4_detail'),
]