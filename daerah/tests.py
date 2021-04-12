from django.db.models.functions import Length
from django.test import TestCase

from daerah.models import Daerah


def status_daerah(kode):
    wilayah = kode.split('.')
    if len(wilayah) == 1:
        return 'Propinsi'
    elif len(wilayah) == 2:
        if wilayah[1][0] == '0':
            return 'Kabupaten'
        elif wilayah[1][0] == '7':
            return 'Kotamadya'
    elif len(wilayah) == 3:
        return 'Kecamatan'
    elif len(wilayah) == 4:
        if wilayah[3][0] == '1':
            return 'Kelurahan'
        if wilayah[3][0] == '2':
            return 'Desa'


class DaerahTestCase(TestCase):
    fixtures = ['domisili.json']

    def test_daerah_read_all(self):
        daerah = Daerah.objects.all()
        self.assertEqual(daerah.count(), 91219)

    def test_daerah_limit_by_nama(self):
        pilihan = 'ACEH'
        try:
            daerah = Daerah.objects.get(nama=pilihan)
        except Daerah.DoesNotExist:
            daerah = None
        if daerah is not None:
            self.assertEqual(daerah.nama, pilihan)

    def test_daerah_limit_by_propinsi(self):
        daerah = Daerah.objects.annotate(length=Length('kode')).filter(length=2)
        self.assertEqual(daerah.count(), 34)

    def test_daerah_search_kabupaten_by_propinsi(self):
        propinsi = Daerah.objects.annotate(length=Length('kode')).filter(length=2).order_by('?').first()
        kabupaten = Daerah.objects.annotate(length=Length('kode')).filter(length=5, kode__startswith=propinsi.kode)
        self.assertTrue(kabupaten.exists())
        for k in kabupaten:
            self.assertTrue(propinsi.kode in k.kode)

    def test_daerah_search_kecamatan_by_kabupaten(self):
        propinsi = Daerah.objects.annotate(length=Length('kode')).filter(length=2).order_by('?').first()
        kabupaten = Daerah.objects.annotate(length=Length('kode')) \
            .filter(length=5, kode__startswith=propinsi.kode).order_by('?').first()
        kecamatan = Daerah.objects.annotate(length=Length('kode')).filter(length=8, kode__startswith=kabupaten.kode)
        self.assertTrue(kecamatan.exists())
        for kec in kecamatan:
            self.assertTrue(kabupaten.kode in kec.kode)

    def test_daerah_search_desa_by_kecamatan(self):
        propinsi = Daerah.objects.annotate(length=Length('kode')).filter(length=2).order_by('?').first()
        kabupaten = Daerah.objects.annotate(length=Length('kode')) \
            .filter(length=5, kode__startswith=propinsi.kode).order_by('?').first()
        kecamatan = Daerah.objects.annotate(length=Length('kode')) \
            .filter(length=8, kode__startswith=kabupaten.kode).order_by('?').first()
        kelurahan = Daerah.objects.annotate(length=Length('kode')).filter(length=13, kode__startswith=kecamatan.kode)
        self.assertTrue(kelurahan.exists())
        for kel in kelurahan:
            self.assertTrue(kecamatan.kode in kel.kode)

    def test_daerah_status_equal_propinsi(self):
        pilihan = 'ACEH'
        daerah = Daerah.objects.filter(nama=pilihan)
        status = status_daerah(daerah[0].kode)
        self.assertEqual(status, 'Propinsi')

    def test_daerah_status_equal_kabupaten(self):
        pilihan = 'KAB. ACEH SELATAN'
        daerah = Daerah.objects.filter(nama=pilihan)
        status = status_daerah(daerah[0].kode)
        self.assertEqual(status, 'Kabupaten')

    def test_daerah_status_equal_kecamatan(self):
        pilihan = 'Bakongan'
        daerah = Daerah.objects.filter(nama=pilihan)
        status = status_daerah(daerah[0].kode)
        self.assertEqual(status, 'Kecamatan')

    def test_daerah_status_equal_desa(self):
        pilihan = 'Keude Bakongan'
        daerah = Daerah.objects.filter(nama=pilihan)
        status = status_daerah(daerah[0].kode)
        self.assertEqual(status, 'Desa')
