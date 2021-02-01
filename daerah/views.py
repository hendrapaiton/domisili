from django.db.models.functions import Length
from rest_framework import mixins, generics

from daerah.models import Daerah
from daerah.serializers import DaerahSerializer


class PropinsiList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Daerah.objects.annotate(length=Length('kode')).filter(length=2)
    serializer_class = DaerahSerializer

    def get(self, request):
        return self.list(request)
