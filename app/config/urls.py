from django.contrib import admin
from django.urls import path, include
from daireler.views import panel, fatura_pdf, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Giriş / çıkış
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # API endpointleri
    path('api/', include('daireler.urls')),

    # Panel
    path('', panel, name='panel'),

    # PDF fatura indir
    path('fatura/<int:fatura_id>/pdf/', fatura_pdf, name='fatura_pdf'),
]