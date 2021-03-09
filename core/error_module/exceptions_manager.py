import json
import os

from core.error_module.api_exceptions import ApiExceptions
from core.error_module.exceptions import Exceptions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(BASE_DIR, "settings/error_constants.json")) as f:
    data = json.load(f)


class ExceptionsManager:
    def __init__(self, params):
        self.error_type = params['error_type']
        self.params = params

    def generate_exception(self):
        if self.error_type == "API":
            exception_object = ApiExceptions(self.params['code'], self.params['message'])
            return exception_object.get_error_object()

        code = data['GENERAL_EXCEPTION']['UNKNOWN_ERROR']['CODE']
        message = data['GENERAL_EXCEPTION']['UNKNOWN_ERROR']['MESSAGE']
        exceptions_object = Exceptions(code, message)
        return exceptions_object.get_error_object()
