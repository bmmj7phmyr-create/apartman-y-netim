from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from xhtml2pdf import pisa
from rest_framework import viewsets

from .models import Daire, Fatura, IzsuFaturaTakip
from .serializers import DaireSerializer, FaturaSerializer, IzsuFaturaTakipSerializer


AYLAR = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık",
}


def login_view(request):
    if request.user.is_authenticated:
        return redirect("panel")

    hata_mesaji = ""

    if request.method == "POST":
        kullanici_id = request.POST.get("username", "").strip()
        sifre = request.POST.get("password", "").strip()

        user = authenticate(request, username=kullanici_id, password=sifre)

        if user is not None:
            login(request, user)
            return redirect("panel")
        else:
            hata_mesaji = "ID veya şifre hatalı."

    return render(request, "panel/login.html", {"hata_mesaji": hata_mesaji})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("panel")


@method_decorator(login_required, name='dispatch')
class DaireViewSet(viewsets.ModelViewSet):
    queryset = Daire.objects.all()
    serializer_class = DaireSerializer


@method_decorator(login_required, name='dispatch')
class FaturaViewSet(viewsets.ModelViewSet):
    queryset = Fatura.objects.all().order_by('-id')
    serializer_class = FaturaSerializer


@login_required
def panel(request):
    return render(request, 'panel/index.html')


@login_required
def fatura_pdf(request, fatura_id):
    fatura = get_object_or_404(Fatura, id=fatura_id)

    ay_yil = f"{AYLAR.get(fatura.ay, fatura.ay)} {fatura.yil}"

    context = {
        "fatura": fatura,
        "ay_yil": ay_yil,
        "onceki_endeks": fatura.onceki_endeks or 0,
        "simdiki_endeks": fatura.simdiki_endeks or 0,
        "tuketilen_metrekup": fatura.tuketilen_metrekup or 0,
        "birim_fiyat": fatura.birim_fiyat or 0,
        "tutar": fatura.tutar or 0,
        "hizmet_bedeli": fatura.hizmet_bedeli or 0,
        "eski_borc": fatura.eski_borc or 0,
        "toplam_tutar": fatura.toplam_tutar or 0,
    }

    template = get_template("panel/fatura_pdf.html")
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="fatura_{fatura.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse("PDF oluşturulamadı.")
    return response


@method_decorator(login_required, name='dispatch')
class IzsuFaturaTakipViewSet(viewsets.ModelViewSet):
    queryset = IzsuFaturaTakip.objects.all().order_by('-olusturma_tarihi')
    serializer_class = IzsuFaturaTakipSerializer