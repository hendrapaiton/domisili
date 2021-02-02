from django.urls import path

from daerah import views

urlpatterns = [
    path('propinsi/', views.Propinsi.as_view(), name='Propinsi'),
    path('propinsi/<str:prop>/kabupaten/', views.Kabupaten.as_view(), name='Kabupaten'),
    path('propinsi/<str:prop>/kabupaten/<str:kab>/kecamatan/', views.Kecamatan.as_view(), name='Kecamatan'),
    path('propinsi/<str:prop>/kabupaten/<str:kab>/kecamatan/<str:kec>/kelurahan/',
         views.Kelurahan.as_view(),
         name='kelurahan'),
    path('wilayah/<str:kode>/', views.Wilayah.as_view(), name='Wilayah'),
]
