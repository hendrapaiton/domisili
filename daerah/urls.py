from django.urls import path

from daerah import views

urlpatterns = [
    path('api/propinsi/', views.PropinsiList.as_view(), name='Propinsi'),
]
