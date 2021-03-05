import json
import os
from core.error_module.Exceptions import Exceptions

HTTP_STATUS_CODES = {
    404: "NOT_FOUND",
    401: "UNAUTHORIZED",
    200: "SUCCESS",
    403: "FORBIDDEN"
}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open("settings/error_constants.json") as f:
    data = json.load(f)
f.close()


class ApiExceptions(Exceptions):
    def __init__(self, code, message):
        super().__init__(code, message)

    def get_error_object(self):
        error_obj = {}
        if self.code:
            error_obj['status'] = False
            error_obj['error_code'] = self.code
            error_obj['error_message'] = self.message.lower()
            error_obj['data'] = ""
        else:
            error_obj['status'] = False
            error_obj['error_code'] = data['API_ERRORS']['UNKNOWN_ERROR']['CODE']
            error_obj['error_message'] = data['API_ERRORS']['UNKNOWN_ERROR']['MESSAGE']
            error_obj['data'] = ""
        return error_obj
