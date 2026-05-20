
from django.contrib import admin
from django.urls import include, path
from . import views

app_name='movies'
urlpatterns= [ 
    path('', views.list_movies, name='movies_list'),
    path('list/', views.list_movies, name='movies_list'),
    path('list/<int:id>/', views.list_movie_By_ID, name='movie_by_id'),
    path('edit/<int:id>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:id>/', views.delete_movie, name='delete_movie'),
    path('add/', views.add_movie, name='add_movie'),
    # api/v1: FBV
    path('api/v1/', views.movie_api_list, name='v1_list'),
    path('api/v1/<int:id>/', views.movie_api_detail, name='v1_detail'),
    # api/v2: CBV
    path('api/v2/', views.MovieListCBV.as_view(), name='v2_list'),
    path('api/v2/<int:id>/', views.MovieDetailCBV.as_view(),name='v2_detail'),
    # api/v3: Mixins
    path('api/v3/', views.MovieListMixins.as_view(), name='v3_list'),
    path('api/v3/<int:id>/', views.MovieDetailMixins.as_view(), name='v3_detail'),
    # api/v4: Generic Views 
    path('api/v4/', views.MovieListGeneric.as_view(), name='v4_list'),
    path('api/v4/<int:id>/', views.MovieDetailGeneric.as_view(), name='v4_detail'),

]