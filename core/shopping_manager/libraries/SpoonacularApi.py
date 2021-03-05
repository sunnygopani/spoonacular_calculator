import os
from dotenv import load_dotenv
import json
import requests  # To use request package in current program
from core.error_module.ExceptionsManager import ExceptionsManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

with open(os.path.join(BASE_DIR, "settings/constants.json")) as f:
    data = json.load(f)
f.close()
load_dotenv()


class SpoonacularApi:
    api_key = os.getenv('SPOONACULAR_API_KEY')
    api_base_url = data['BASE_URL']

    def __init__(self):
        pass

    def search_recipies_by_ingredients(self, params):
        resource = data['APIS']['FIND_BY_INGREDIENTS']
        url = self.api_base_url + resource['PATH']
        query = self.extract_fixed_params(resource['PARAMS'])
        query[params['key']] = self.extract_list_params(params)
        response = self.http_request(url, resource['METHOD'], query)
        return response

    def get_recipe_details(self, params):
        resource = data['APIS']['FIND_BY_INGREDIENT']
        url = self.api_base_url + resource['PATH']
        query = self.extract_fixed_params(resource['PARAMS'])
        query[params['key']] = self.extract_list_params(params)
        response = self.http_request(url, resource['METHOD'], query)
        return response

    def get_ingredient_details(self, params):
        resource = data['APIS']['GET_INGREDIENT']
        url = self.api_base_url + resource['PATH'] + '/' + str(params['id']) + '/information'
        del params['id']
        params['apiKey'] = SpoonacularApi.api_key
        response = self.http_request(url, resource['METHOD'], params)
        return response

    @staticmethod
    def extract_fixed_params(params: any):
        query = dict()
        for items in params:
            query[items['NAME']] = items['VALUE']
        query['apiKey'] = SpoonacularApi.api_key
        return query

    @staticmethod
    def extract_list_params(params: any):
        extracted_params = ""
        for i in range(len(params['values'])):
            extracted_params = extracted_params + str(params['values'][i])
            if i < len(params['values']) - 1:
                extracted_params = extracted_params + ','
        return extracted_params

    @staticmethod
    def http_request(url, method, params):
        try:
            api_response = {}
            if method == 'GET':
                api_response = requests.get(url, params)  # To execute get request
                if api_response.status_code != 200:
                    error_params = {'error_type': 'API', 'code': api_response.status_code, 'message': 'Unable to reach '
                                                                                                      'the Spoonacular '
                                                                                                      'server'}
                    ex_manager_obj = ExceptionsManager(error_params)
                    error_object = ex_manager_obj.generate_exception()
                    return error_object
                if len(api_response.json()) < 1:
                    error_params = \
                        {'error_type': 'API', 'code': 2001, 'message': 'No results found for the given input'}
                    ex_manager_obj = ExceptionsManager(error_params)
                    error_object = ex_manager_obj.generate_exception()
                    return error_object
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            return error_object
        response = {
            "status": True,
            "error_code": 0,
            "error_message": "",
            "data": api_response.json()
        }
        return response
