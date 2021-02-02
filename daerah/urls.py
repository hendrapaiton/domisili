from django.urls import path

from daerah import views

urlpatterns = [
    path('propinsi/', views.Propinsi.as_view(), name='Propinsi'),
    path('propinsi/<str:kode>/kabupaten/', views.Kabupaten.as_view(), name='Kabupaten'),
]
