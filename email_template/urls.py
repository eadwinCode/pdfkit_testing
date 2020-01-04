from django.contrib import admin
from django.urls import path, include
from .views import GenerateDownloadLink, DownloadPDFView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('account/agreement', GenerateDownloadLink.as_view(), name='agreement'),
    # use something unique to use as url parameter <str:email>
    path('account/agreement/<str:email>/pdf', DownloadPDFView.as_view(), name='pdf-download')
]
