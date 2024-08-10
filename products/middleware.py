from django.utils.deprecation import MiddlewareMixin
from .utils import encrypt_data, decrypt_data
import logging

logger = logging.getLogger(__name__)

class EncryptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.body and request.content_type == 'application/json':
            try:
                logger.debug(f"Encrypted request body: {request.body.decode('utf-8')}")
                decrypted_body = decrypt_data(request.body.decode('utf-8'))
                logger.debug(f"Decrypted request body: {decrypted_body}")
                request.body = decrypted_body.encode('utf-8')
            except Exception as e:
                logger.error(f"Decryption error: {e}")
                raise
        response = self.get_response(request)
        if response.content and response['Content-Type'] == 'application/json':
            try:
                encrypted_content = encrypt_data(response.content.decode('utf-8'))
                logger.debug(f"Encrypted response content: {encrypted_content}")
                response.content = encrypted_content.encode('utf-8')
            except Exception as e:
                logger.error(f"Encryption error: {e}")
                raise
        return response
