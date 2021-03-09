from core.helpers.formatter import *
from core.shopping_manager.classes.recipe_manager import *
from core.shopping_manager.classes.invoice import *

# Importing all the necessary modules for the project execution
log_object = Logger()
log_handler = log_object.get_logger()


# Getting the logging handler so as to add the logs in the required locations of the code


def main(args=''):
    # Main method to present the different options for the end user to get the recipes for the ingredients.
    try:
        # Invoice object to access the methods of the Invoice class so as to
        # compute the total estimated cost of all the missing ingredients.
        invoice_obj = Invoice()
        # Display a welcome message to the end user.
        display_welcome_message()
        while True:
            # Set of operations to be performed until the end user chooses to exit the application
            # or in case the application is not able to reach the Spoonacular server.

            # Use the list of ingredients if they have been
            # passed as an argument at the time of invocation of the main().
            # Else, scan the list of ingredients from the end user.
            if args:
                ingredients_list = args
            else:
                ingredients_list = user_ingredients_input()
            # If the user chooses to exit the application, return
            if ingredients_list[0] == 'e':
                break
            # Display a message that indicates the request is being processed.
            display_processing_message(ingredients_list)
            # Recipe manager object to access the methods from the RecipeManager class
            # to communicate with Spoonacluar API library and format the response.
            recipe_manager_object = RecipeManager()
            # Obtain the list of all the 100 recipes comprising details that include name, id
            # and the list of missing ingredients comprising details that include id, name, amount, aisle, unit.
            recipes = recipe_manager_object.get_all_recipes(ingredients_list)
            # If get_all_recipes did not execute successfully,
            # display the appropriate error message and ask the end user to try again
            # in case the issue is related to the data that the end user entered.
            if not recipes['status']:
                display_error_message(recipes)
            else:
                # Create an iterator to iterate through the list of recipes
                recipe_iterator = (item for item in recipes['data'])
                # Using while loop so that if there is no next recipe available,
                # the iterator returns an exception which has been caught and handled appropriately.
                # Repeat the set of operations until there is no recipe left or if the end user chooses to exit.
                while True:
                    try:
                        # Record the next recipe's name and id so as to fetch the remaining details about the recipe.
                        next_recipe = next(recipe_iterator)
                        # Obtain the actual recipe instructions.
                        recipe_details = recipe_manager_object.get_recipe(next_recipe['id'])
                        # In case of an error returned from the get_recipe function,
                        # display the appropriate error message and ask the end user to try again.
                        # The errors are logged under the logs folder for further debugging.
                        if not recipe_details['status']:
                            display_error_message(recipe_details)
                            break
                        # Add instructions to the next recipe dictionary
                        next_recipe.update(recipe_details['data'])
                        # Display the recipe with an appropriate format
                        display_recipe(next_recipe)
                        # Ask if the user likes the recipe
                        status_of_like = user_like_input()
                        # If the end user likes the recipe, obtain the missing ingredient details like quantity (amount)
                        # and the total cost of all the missing ingredients recorded so far.
                        if status_of_like.lower() in ('y'.lower(), 'yes'.lower()):
                            # If missingIngredients key exists, perform the next steps.
                            if 'missedIngredients' in next_recipe.keys():
                                for missing_ingredient in next_recipe['missedIngredients']:
                                    # Fetch the ingredient information
                                    ingredient_details = recipe_manager_object.get_ingredient(
                                        {'id': missing_ingredient.get('id', 0),
                                         'amount': missing_ingredient.get('amount', 0),
                                         'unit': missing_ingredient.get('unit', '')})
                                    # In case of an error returned from the get_ingredient function,
                                    # display the appropriate error message and ask the end user to try again.
                                    if not ingredient_details['status']:
                                        display_error_message(ingredient_details)
                                        break
                                    shopping_cart = {
                                        'id': str(missing_ingredient['id']),
                                        'item': missing_ingredient.get('name', ''),
                                        'amount': missing_ingredient.get('amount', 0),
                                        'aisle': missing_ingredient.get('aisle', ''),
                                        'cost': {
                                            'value': ingredient_details['data'].get('cost', 0).get('value', 0),
                                            'unit': ingredient_details['data'].get('cost', 'NA').get('unit', 'NA')
                                        }
                                    }
                                    # Add missing ingredients to the shopping cart
                                    invoice_obj.add_items(shopping_cart)
                                # Display the menu with four different choices that include show next recipe,
                                # take new set of ingredients, display shopping cart and exit.
                                while True:
                                    display_menu()
                                    choice = user_menu_input()
                                    if choice == 'e':
                                        # If the user types e, show the exit message and quit from the application.
                                        display_exit_message()
                                        return
                                    elif choice == 'n':
                                        # If the user types n, get the next recipe
                                        break
                                    elif choice == 'r':
                                        # If the user types r, get the next set of ingredients
                                        break
                                    elif choice == 's':
                                        # If the user types s, display the most recent
                                        # shopping cart with a pretty format.
                                        display_shopping_cart(invoice_obj.final_shopping_list, invoice_obj.total_cost)
                                    else:
                                        # Display an appropriate message in case of a wrong choice.s
                                        display_error_message({"error_message": "Wrong choice. Please try again from "
                                                                                "the given "
                                                                                "menu options!"})
                                        continue
                                if choice != 'n':
                                    break
                    except Exception as ex:
                        error_params = {'error_type': 'UNKNOWN', 'message': ex}
                        ex_manager_obj = ExceptionsManager(error_params)
                        error_object = ex_manager_obj.generate_exception()
                        log_handler.error('error_object: {}'.format(error_object))
                        display_list_empty()
                        break

        display_exit_message()
    except Exception as ex:
        error_params = {'error_type': 'UNKNOWN', 'message': ex}
        ex_manager_obj = ExceptionsManager(error_params)
        error_object = ex_manager_obj.generate_exception()
        log_handler.error('error_object: {}'.format(error_object))
        display_error_message(error_object)
        main()


if __name__ == "__main__":
    main()
