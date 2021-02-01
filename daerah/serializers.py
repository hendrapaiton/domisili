from rest_framework import serializers

from daerah.models import Daerah


class DaerahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Daerah
        fields = ('kode', 'nama')
