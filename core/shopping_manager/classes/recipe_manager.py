from core.error_module.exceptions_manager import ExceptionsManager
from core.helpers.spoonacular_logger import Logger
from core.shopping_manager.libraries.spoonacular_api import SpoonacularApi
from cerberus import Validator


# Import the required modules
# Using cerberus module for validating the inputs


class RecipeManager:
    def __init__(self) -> None:
        # Get the logging handler
        self.log_object = Logger()
        self.log_handler = self.log_object.get_logger()
        # Get the Spoonacular API object that communicates with Spoonacular server to get the list of recipes
        self.spoonacular_obj = SpoonacularApi()

    def get_all_recipes(self, ingredients: dict) -> dict:
        # Handler to obtain all the recipes by passing inputs in the required
        # format and returning response in an appropriate format.
        try:
            if not isinstance(ingredients, list):
                raise Exception("Ingredients need to be a list of values")
            self.log_handler.debug('Ingredients: {}'.format(ingredients))
            # Obtain the list of all the recipes based on the ingredients.
            response = self.spoonacular_obj.search_recipies_by_ingredients({'ingredients': ingredients})
            # Extract the required fields from the response using the map function
            # such that it filter outs the unwanted fields.
            response['data'] = list(map(self.project_recipe_data, response['data']))
        except Exception as ex:
            print(str(ex))
            error_params = {'error_type': 'UNKNOWN', 'message': str(ex)}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object
        return response

    def get_recipe(self, recipe_id: int) -> dict:
        # Handler to obtain the recipe information by passing inputs in the required
        # format and returning response in an appropriate format.
        try:
            # Input validation
            if not recipe_id or not isinstance(recipe_id, int):
                raise Exception("ids need to be in string format")
            self.log_handler.debug('ids: {}'.format(recipe_id))
            # Fetch the recipe information
            response = self.spoonacular_obj.get_recipe_details({'ids': recipe_id})
            self.log_handler.debug('response: {}'.format(response))
            response['data'] = self.project_recipe_summary(response['data'][0])
            # Format the response in a standard format.
            return response
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object

    def get_ingredient(self, params):
        # Handler to obtain the ingredient information by passing inputs in the required
        # format and returning response in an appropriate format.
        try:
            # Input validation
            get_get_ingredient = {
                'id': {
                    'type': 'integer'
                },
                'amount': {
                    'type': 'float',
                    'required': False
                },
                'unit': {
                    'type': 'string',
                    'required': False
                }
            }
            v = Validator(get_get_ingredient)
            v.validate(params)
            self.log_handler.debug('params: {}'.format(params))
            # Fetch the ingredient information
            response = self.spoonacular_obj.get_ingredient_details(params)
            self.log_handler.debug('response: {}'.format(response))
            response['data'] = self.project_ingredient_details(response['data'])
            return response
        except Exception as ex:
            error_params = {'error_type': 'UNKNOWN', 'message': ex}
            ex_manager_obj = ExceptionsManager(error_params)
            error_object = ex_manager_obj.generate_exception()
            self.log_handler.error('error_object: {}'.format(error_object))
            return error_object

    def project_recipe_data(self, data):
        try:
            # Function to format the response fetched from search_recipies_by_ingredients function.
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
        # Method to format the response fetched from get_ingredient_details function.
        return {
            'amount': data.get('amount', 0),
            'cost': {
                'value': data.get('estimatedCost', 0).get('value', 0),
                'unit': data.get('estimatedCost', 'NA').get('unit', 'NA')
            }
        }

    @staticmethod
    def project_recipe_summary(data):
        # Method to format the response fetched from get_recipe function.
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
        # Method to format the ingredients list fetched from search_recipies_by_ingredients function.
        return {
            'id': data.get('id', 'NA'),
            'name': data.get('name', 'NA'),
            'amount': data.get('amount', 0),
            'aisle': data.get('aisle', 'NA'),
            'unit': data.get('unit', 'NA')
        }
