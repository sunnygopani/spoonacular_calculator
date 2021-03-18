import os
import urllib
import requests
from dotenv import load_dotenv
import json
from core.helpers.spoonacular_logger import Logger
from core.error_module.exceptions_manager import ExceptionsManager

# Import all the required modules
# Load the constants from the settings/constants.json
# file that includes the API base url and parameters for the different APIs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
with open(os.path.join(BASE_DIR, "settings/constants.json")) as f:
    data = json.load(f)
f.close()
load_dotenv()


class SpoonacularApi:
    """
    Class to interact with the Spoonacular API
    """
    def __init__(self, api_auth_params={}):
        # Initialize logging handler, api base url and api key to be used in the subsequent request.
        self.log_object = Logger()
        self.log_handler = self.log_object.get_logger()
        self.log_handler.debug('Params: {}'.format(api_auth_params))
        # Extract the Api Key from the .env file
        self.api_key = api_auth_params.get('api_key', os.getenv('SPOONACULAR_API_KEY'))
        self.api_base_url = api_auth_params.get('api_base_url', data['BASE_URL'])

    def search_recipies_by_ingredients(self, params) -> dict:
        # Implementation of the Spoonacular API - recipes/findByIngredients.
        """
        Returns list of all the recipes for the given ingredients
        :param params: {"ingredients":<comma seperated list of ingredients> "apple, eggs"}
        :return: dict object {"status":bool, "error_message":string, "error_code":int, "data": <array of recipes>}
        """
        try:
            self.log_handler.debug('Params: {}'.format(params))
            resource = data['APIS']['FIND_BY_INGREDIENTS']
            self.log_handler.debug('resource: {}'.format(resource))
            url = self.api_base_url + resource['PATH']
            self.log_handler.debug('url: {}'.format(url))
            body = resource['PARAMS']
            body.update(params)
            self.log_handler.debug('body: {}'.format(body))
            response = self.http_request(url, resource['METHOD'], body)
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object
        return response

    def get_recipe_details(self, params):
        # Implementation of the Spoonacular API - recipes/informationBulk.
        try:
            self.log_handler.debug('Params: {}'.format(params))
            resource = data['APIS']['FIND_BY_INGREDIENT']
            self.log_handler.debug('resource: {}'.format(resource))
            url = self.api_base_url + resource['PATH']
            body = resource['PARAMS']
            body.update(params)
            self.log_handler.debug('body: {}'.format(body))
            response = self.http_request(url, resource['METHOD'], body)
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object
        return response

    def get_ingredient_details(self, params):
        try:
            # Implementation of the Spoonacular API - food/ingredients.
            self.log_handler.debug('params: {}'.format(params))
            resource = data['APIS']['GET_INGREDIENT']
            self.log_handler.debug('resource: {}'.format(resource))
            url = self.api_base_url + resource['PATH'] + '/' + str(params['id']) + '/information'
            self.log_handler.debug('url: {}'.format(url))
            del params['id']
            response = self.http_request(url, resource['METHOD'], params)
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object
        return response

    def http_request(self, url, method, body):
        try:
            # Function to create an HTTP request with an external
            # end point with the help of api url, method and body.
            self.log_handler.debug('url: {}'.format(url))
            self.log_handler.debug('method: {}'.format(method))
            api_response = {}
            body['apiKey'] = self.api_key
            self.log_handler.debug('body: {}'.format(body))
            if method == 'GET':
                url_values = urllib.parse.urlencode(body)
                full_url = url + '?' + url_values
                self.log_handler.debug('full_url: {}'.format(full_url))
                api_response = requests.get(full_url)
                # In case of any HTTP error, raise an exception and send it to the exceptions manager
                api_response.raise_for_status()
                # If no results returned, create an exception and send it to the exceptions manager
                if not api_response.json():
                    error_params = \
                        {'error_type': 'API', 'code': 2001, 'message': 'No results found for the given input'}
                    ex_manager_obj = ExceptionsManager(error_params)
                    error_object = ex_manager_obj.generate_exception()
                    self.log_handler.error('error_object: {}'.format(error_object))
                    return error_object
        except requests.HTTPError as ex:
            error_params = {'error_type': 'API', 'message': str(ex), 'code': ex.response.status_code}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object
        return {
            "status": True,
            "error_code": 0,
            "error_message": "",
            "data": api_response.json()
        }
