import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daireler', '0003_remove_fatura_calisma_bedeli_fatura_hizmet_bedeli'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='daire',
            name='mevcut_metrekup_tuketimi',
        ),
        migrations.RemoveField(
            model_name='fatura',
            name='olusturma_tarihi',
        ),
        migrations.AddField(
            model_name='daire',
            name='ad_soyad',
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='daire',
            name='bina_no',
            field=models.CharField(default="", max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fatura',
            name='odeme_tarihi',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fatura',
            name='onceki_endeks',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fatura',
            name='simdiki_endeks',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fatura',
            name='tarih',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='fatura',
            name='toplam_tutar',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='fatura',
            name='hizmet_bedeli',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fatura',
            name='tuketilen_metrekup',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]