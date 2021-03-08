from core.helpers.formatter import *
from core.shopping_manager.classes.recipe_manager import *
from core.shopping_manager.classes.invoice import *


def main():
    try:
        shopping_cart = {}
        invoice_obj = Invoice()
        display_welcome_message()
        while True:
            ingredients_list = user_ingredients_input()
            if ingredients_list[0] == 'e':
                break
            display_processing_message(ingredients_list)
            recipe_manager_object = RecipeManager()
            recipes = recipe_manager_object.get_all_recipes(ingredients_list)
            if not recipes['status']:
                display_error_message(recipes)
            else:
                recipe_iterator = iter(recipes['data'])
                for next_recipe in recipe_iterator:
                    recipe_details = recipe_manager_object.get_recipe(next_recipe['id'])
                    if not recipe_details['status']:
                        display_error_message(recipe_details)
                        break
                    next_recipe.update(recipe_details['data'])
                    display_recipe(next_recipe)
                    status_of_like = user_like_input()
                    if status_of_like.lower() in ('y'.lower(), 'yes'.lower()):
                        for missing_ingredient in next_recipe['missedIngredients']:
                            ingredient_details = recipe_manager_object.get_ingredient(
                                {'id': missing_ingredient.get('id', ''), 'amount': missing_ingredient.get('amount', ''),
                                 'unit': missing_ingredient.get('unit', '')})
                            if not ingredient_details['status']:
                                display_error_message(ingredient_details)
                                break
                            shopping_cart[str(missing_ingredient['id'])] = {
                                'item': missing_ingredient.get('name', ''),
                                'amount': missing_ingredient.get('amount', ''),
                                'aisle': missing_ingredient.get('aisle', ''),
                                'cost': {
                                    'value': ingredient_details['data'].get('cost', 0).get('value', 0),
                                    'unit': ingredient_details['data'].get('cost', 'NA').get('unit', 'NA')
                                }
                            }
                        invoice_obj.add_items(shopping_cart)
                        while True:
                            display_menu()
                            choice = user_menu_input()
                            if choice == 'e':
                                display_exit_message()
                                return
                            elif choice == 'n':
                                break
                            elif choice == 'r':
                                break
                            elif choice == 's':
                                display_shopping_cart(invoice_obj.final_shopping_list, invoice_obj.total_cost)
                            else:
                                display_error_message({"error_message": "Wrong choice. Please try again from the given "
                                                                        "menu options!"})
                                continue
                        if choice != 'n':
                            break
        display_exit_message()
    except Exception as ex:
        log_object = Logger()
        log_handler = log_object.get_logger()
        error_params = {'error_type': 'UNKNOWN', 'message': ex}
        ex_manager_obj = ExceptionsManager(error_params)
        error_object = ex_manager_obj.generate_exception()
        log_handler.error('error_object: {}'.format(error_object))
        display_error_message(error_object)
        main()


if __name__ == "__main__":
    main()
