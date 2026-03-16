from django.db import models
from django.utils import timezone


class Daire(models.Model):
    ad_soyad = models.CharField(max_length=100)
    bina_no = models.CharField(max_length=20)
    daire_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.ad_soyad} - Daire {self.daire_no}"


class Fatura(models.Model):
    ODEME_DURUMLARI = [
        ('odendi', 'Ödendi'),
        ('odenmedi', 'Ödenmedi'),
    ]

    daire = models.ForeignKey(Daire, on_delete=models.CASCADE, related_name='faturalar')

    tarih = models.CharField(max_length=20, blank=True, null=True)  # 13.03.2026 gibi girilebilsin
    onceki_endeks = models.DecimalField(max_digits=10, decimal_places=2)
    simdiki_endeks = models.DecimalField(max_digits=10, decimal_places=2)
    tuketilen_metrekup = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    birim_fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    hizmet_bedeli = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    eski_borc = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    tutar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    toplam_tutar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    ay = models.PositiveIntegerField()
    yil = models.PositiveIntegerField()

    odeme_durumu = models.CharField(max_length=20, choices=ODEME_DURUMLARI, default='odenmedi')
    odeme_tarihi = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.tuketilen_metrekup = abs(self.simdiki_endeks - self.onceki_endeks)
        self.tutar = self.tuketilen_metrekup * self.birim_fiyat
        self.toplam_tutar = self.tutar + self.hizmet_bedeli + (self.eski_borc or 0)

        if self.odeme_durumu == 'odendi' and not self.odeme_tarihi:
            self.odeme_tarihi = timezone.localdate()

        if self.odeme_durumu == 'odenmedi':
            self.odeme_tarihi = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.daire.daire_no} - {self.ay}/{self.yil}"

class IzsuFaturaTakip(models.Model):
    ilk_endeks = models.FloatField()
    son_endeks = models.FloatField()
    tuketim = models.FloatField()

    ilk_okuma_tarihi = models.CharField(max_length=50)
    son_okuma_tarihi = models.CharField(max_length=50)

    tuketim_gun_sayisi = models.IntegerField()
    fatura_tutari = models.FloatField()

    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"İZSU Fatura - {self.olusturma_tarihi}"