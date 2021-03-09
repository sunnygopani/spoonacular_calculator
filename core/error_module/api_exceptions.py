import json
import os
from core.error_module.exceptions import Exceptions

HTTP_STATUS_CODES = {
    404: "NOT_FOUND",
    401: "UNAUTHORIZED",
    200: "SUCCESS",
    403: "FORBIDDEN"
}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(BASE_DIR, "settings/error_constants.json")) as f:
    data = json.load(f)
f.close()


class ApiExceptions(Exceptions):
    def __init__(self, code, message):
        super().__init__(code, message)

    def get_error_object(self):
        return {
            'status': False,
            'error_code': self.code if self.code else data['API_ERRORS']['UNKNOWN_ERROR']['CODE'],
            'error_message': self.message.lower() if self.message else data['API_ERRORS']['UNKNOWN_ERROR']['MESSAGE'],
            'data': ''
        }
