from rest_framework import serializers
from .models import Daire, Fatura, IzsuFaturaTakip


class DaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Daire
        fields = '__all__'


class FaturaSerializer(serializers.ModelSerializer):
    daire_no = serializers.CharField(source='daire.daire_no', read_only=True)
    ad_soyad = serializers.CharField(source='daire.ad_soyad', read_only=True)
    bina_no = serializers.CharField(source='daire.bina_no', read_only=True)

    class Meta:
        model = Fatura
        fields = '__all__'
        read_only_fields = ['tuketilen_metrekup', 'tutar', 'toplam_tutar', 'odeme_tarihi']


class IzsuFaturaTakipSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzsuFaturaTakip
        fields = "__all__"
        read_only_fields = ['olusturma_tarihi']