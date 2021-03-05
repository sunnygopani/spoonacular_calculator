from core.shopping_manager.libraries.SpoonacularApi import SpoonacularApi


class RecipeManager:
    def __init__(self):
        pass

    def get_all_recipes(self, ingredients):
        params = {'key': 'ingredients', 'values': ingredients}
        spoonacular_obj = SpoonacularApi()
        response = spoonacular_obj.search_recipies_by_ingredients(params)
        response['data'] = list(map(self.project_recipe_data, response['data']))
        return response

    def get_recipe(self, ingredients):
        params = {'key': 'ids', 'values': ingredients}
        spoonacular_obj = SpoonacularApi()
        response = spoonacular_obj.get_recipe_details(params)
        if response['status']:
            response = self.project_recipe_summary(response['data'][0])
        return response

    def get_ingredient(self, params):
        spoonacular_obj = SpoonacularApi()
        response = spoonacular_obj.get_ingredient_details(params)
        if response['status']:
            response = self.project_ingredient_details(response['data'])
        return response

    def project_recipe_data(self, data):
        recipes = {}
        if data['id']:
            recipes['id'] = data['id']
        if data['title']:
            recipes['name'] = data['title']
        else:
            recipes['name'] = 'NA'
        if data['missedIngredients']:
            ingredients = map(self.project_ingredient_data, data['missedIngredients'])
            recipes['missedIngredients'] = list(ingredients)
        else:
            recipes['missedIngredients'] =[]
        return recipes

    @staticmethod
    def project_ingredient_details(data):
        ingredient = {}
        if data['amount']:
            ingredient['amount'] = data['amount']
        else:
            ingredient['amount'] = 0
        if data['estimatedCost']:
            ingredient['cost'] = {}
            ingredient['cost']['value'] = data['estimatedCost']['value']
            ingredient['cost']['unit'] = data['estimatedCost']['unit']
        else:
            ingredient['cost'] = {}
        return ingredient

    @staticmethod
    def project_recipe_summary(data):
        message = ""
        if len(data['analyzedInstructions']) > 0:
            for instructionKeys in data['analyzedInstructions']:
                if len(instructionKeys['steps']):
                    for items in instructionKeys['steps']:
                        message += "\n" \
                                   "{}. " \
                                   "{}.".format(items['number'], items['step'])
                else:
                    message = 'NA'
        else:
            message = 'NA'
        return {'instructions': message}

    @staticmethod
    def project_ingredient_data(data):
        ingredients = {}
        if data['id']:
            ingredients['id'] = data['id']
        if data['name']:
            ingredients['name'] = data['name']
        else:
            ingredients['name'] = 'NA'
        if data['amount']:
            ingredients['amount'] = data['amount']
        else:
            ingredients['amount'] = 0
        if data['aisle']:
            ingredients['aisle'] = data['aisle']
        else:
            ingredients['aisle'] = 'NA'
        return ingredients
