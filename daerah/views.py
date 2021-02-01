from django.db.models.functions import Length
from rest_framework.generics import ListAPIView

from daerah.models import Daerah
from daerah.serializers import DaerahSerializer


class Propinsi(ListAPIView):
    queryset = Daerah.objects.annotate(length=Length('kode')).filter(length=2)
    serializer_class = DaerahSerializer
