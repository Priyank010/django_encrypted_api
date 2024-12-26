import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer

# Load the encryption key from the environment variable and decode from Base64
ENCRYPTION_KEY = base64.b64decode(os.getenv("ENCRYPTION_KEY"))

def encrypt_data(data):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Ensure padding to make data length a multiple of block size
    padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)  # PKCS7 padding
    encrypted = encryptor.update(padded_data.encode()) + encryptor.finalize()
    
    # Return IV + encrypted content as Base64
    return base64.b64encode(iv + encrypted).decode()

class EncryptedMessageView(APIView):
    def get(self, request, *args, **kwargs):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        encrypted_data = encrypt_data(str(serializer.data))
        return Response({"encrypted_data": encrypted_data}, status=status.HTTP_200_OK)
