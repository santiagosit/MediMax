from django.urls import path
from .views import BasculaView

from django.urls import path
from .views import BasculaView

urlpatterns = [
    path('peso/', BasculaView.as_view(), name='peso'),
]
