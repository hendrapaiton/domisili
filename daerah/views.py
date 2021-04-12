from django.db.models.functions import Length
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from daerah.models import Daerah
from daerah.serializers import DaerahSerializer


class Propinsi(ListAPIView):
    queryset = Daerah.objects.annotate(length=Length('kode')).filter(length=2)
    serializer_class = DaerahSerializer


class Kabupaten(ListAPIView):
    lookup_field = 'kode'
    serializer_class = DaerahSerializer

    def get_queryset(self):
        prop = self.kwargs.get('prop')
        queryset = Daerah.objects.annotate(length=Length('kode')).filter(length=5, kode__startswith=prop)
        return queryset


class Kecamatan(ListAPIView):
    lookup_field = 'kode'
    serializer_class = DaerahSerializer

    def get_queryset(self):
        prop = self.kwargs.get('prop')
        kab = self.kwargs.get('kab')
        if prop in kab:
            queryset = Daerah.objects.annotate(length=Length('kode')).filter(length=8, kode__startswith=kab)
            return queryset
        else:
            return self.queryset


class Kelurahan(ListAPIView):
    lookup_field = 'kode'
    serializer_class = DaerahSerializer

    def get_queryset(self):
        prop = self.kwargs.get('prop')
        kab = self.kwargs.get('kab')
        kec = self.kwargs.get('kec')
        if prop in kab and kab in kec:
            queryset = Daerah.objects.annotate(length=Length('kode')).filter(length=13, kode__startswith=kec)
            return queryset
        else:
            return self.queryset


class Wilayah(APIView):
    permission_classes = []

    @staticmethod
    def get(request, kode):
        data = kode.split('.')
        wilayah = ['propinsi', 'kabupaten', 'kecamatan', 'kelurahan']
        json = {'kode': kode}
        k = ''

        for i, d in enumerate(data):
            if i > 0:
                k = k + '.' + d
            else:
                k = d
            try:
                json[wilayah[i]] = Daerah.objects.get(kode=k).nama
            except Daerah.DoesNotExist:
                return Response({'status': 'Daerah tidak ditemukan'})

        return Response(json)
