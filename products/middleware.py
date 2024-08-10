from django.utils.deprecation import MiddlewareMixin
from .utils import decrypt_data, encrypt_data

class EncryptionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.body:
            try:
                request.body = decrypt_data(request.body.decode('utf-8')).encode('utf-8')
            except:
                pass

    def process_response(self, request, response):
        if response.content:
            response.content = encrypt_data(response.content.decode('utf-8')).encode('utf-8')
        return response
