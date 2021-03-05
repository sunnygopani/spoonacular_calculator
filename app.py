from core.helpers.formatter import *
from core.shopping_manager.classes.recipe_manager import *
from core.shopping_manager.classes.invoice import *


def main():
    # Welcome message
    # Ingredient message
    #
    # Input from user
    # Shopping manager
    #     -> If recipes are done
    #         -> ask for another ingredients
    #         -> exit
    #     -> get next recipe
    #     -> show recipe
    #     Input from user for liking, disliking
    #         -> If liked
    #         -> Shopping manager -> Add to the bill
    #         -> Input from user to continue
    #             -> Yes -> continue
    #             -> No -> False
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
        if recipes['status']:
            recipe_iterator = iter(recipes['data'])
            for next_recipe in recipe_iterator:
                recipe_details = recipe_manager_object.get_recipe([next_recipe['id']])
                next_recipe.update(recipe_details)
                display_recipe(next_recipe)
                status_of_like = user_like_input()
                if status_of_like == 'y' or status_of_like == 'Y' or status_of_like == 'yes'.lower() \
                        or status_of_like == 'yes'.upper() or status_of_like == 'yes'.capitalize():
                    for missing_ingredient in next_recipe['missedIngredients']:
                        ingredient_details = recipe_manager_object.get_ingredient({'id': missing_ingredient['id'],
                                                                                   'amount': missing_ingredient[
                                                                                       'amount'] if missing_ingredient[
                                                                                       'amount'] else '',
                                                                                   'unit': missing_ingredient[
                                                                                       'amount'] if missing_ingredient[
                                                                                       'amount'] else ''})
                        shopping_cart[str(missing_ingredient['id'])] = {
                            'item': missing_ingredient['name'],
                            'amount': missing_ingredient['amount'],
                            'aisle': missing_ingredient['aisle']
                        }

                        shopping_cart[str(missing_ingredient['id'])]['amount'] = ingredient_details['amount']
                        shopping_cart[str(missing_ingredient['id'])]['cost'] = {}
                        shopping_cart[str(missing_ingredient['id'])]['cost']['value'] = \
                            ingredient_details['cost']['value']
                        shopping_cart[str(missing_ingredient['id'])]['cost']['unit'] = \
                            ingredient_details['cost']['unit']
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
                            display_shopping_cart(invoice_obj.final_shopping_list, invoice_obj.sum)
                        else:
                            display_error_message({"error_message": "Wrong choice. Please try again from the given "
                                                                    "menu options!"})
                            continue
                    if choice == 'n':
                        continue
                    else:
                        break
        else:
            display_error_message(recipes)
            continue
    display_exit_message()


if __name__ == "__main__":
    main()
