from core.error_module.ExceptionsManager import ExceptionsManager
from core.helpers.spoonacular_logger import Logger
from core.shopping_manager.libraries.SpoonacularApi import SpoonacularApi


class RecipeManager:
    def __init__(self):
        self.log_object = Logger()
        self.log_handler = self.log_object.get_logger()

    def get_all_recipes(self, ingredients):
        try:
            self.log_handler.debug('Ingredients: {}'.format(ingredients))
            params = {'ingredients': ingredients}
            spoonacular_obj = SpoonacularApi()
            response = spoonacular_obj.search_recipies_by_ingredients(params)
            response['data'] = list(map(self.project_recipe_data, response['data']))
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object
        return response

    def get_recipe(self, ids):
        try:
            self.log_handler.debug('ids: {}'.format(ids))
            params = {'ids': ids}
            spoonacular_obj = SpoonacularApi()
            response = spoonacular_obj.get_recipe_details(params)
            self.log_handler.debug('response: {}'.format(response))
            if response['status']:
                return {
                    'status': True,
                    'error_code': 0,
                    'error_message': '',
                    'data': self.project_recipe_summary(response['data'][0])
                }
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object

    def get_ingredient(self, params):
        try:
            self.log_handler.debug('params: {}'.format(params))
            spoonacular_obj = SpoonacularApi()
            response = spoonacular_obj.get_ingredient_details(params)
            self.log_handler.debug('response: {}'.format(response))
            if response['status']:
                return {
                    'status': True,
                    'error_code': 0,
                    'error_message': '',
                    'data': self.project_ingredient_details(response['data'])
                }
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object

    def project_recipe_data(self, data):
        try:
            self.log_handler.debug('data: {}'.format(data))
            return {
                'id': data.get('id', 'NA'),
                'name': data.get('title', 'NA'),
                'missedIngredients': list(map(self.project_ingredient_data, data['missedIngredients']))
            }
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object

    @staticmethod
    def project_ingredient_details(data):
        return {
            'amount': data.get('amount', 0),
            'cost': {
                'value': data.get('estimatedCost', 0).get('value', 0),
                'unit': data.get('estimatedCost', 'NA').get('unit', 'NA')
            }
        }

    @staticmethod
    def project_recipe_summary(data):
        message = 'NA'
        if data['analyzedInstructions']:
            message = ''
            for instructionKeys in data['analyzedInstructions']:
                if instructionKeys['steps']:
                    for items in instructionKeys['steps']:
                        message += "\n" \
                                   "{}. " \
                                   "{}.".format(items['number'], items['step'])
        return {'instructions': message}

    @staticmethod
    def project_ingredient_data(data):
        return {
            'id': data.get('id', 'NA'),
            'name': data.get('name', 'NA'),
            'amount': data.get('amount', 0),
            'aisle': data.get('aisle', 'NA')
        }
