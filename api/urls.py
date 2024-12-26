from django.urls import path
from .views import EncryptedMessageView

urlpatterns = [
    path('messages/', EncryptedMessageView.as_view(), name='encrypted-messages'),
]
