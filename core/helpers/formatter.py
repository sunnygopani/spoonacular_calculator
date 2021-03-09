def display_welcome_message() -> None:
    # Function to display welcome message.
    message = "Welcome to Spoonacular." \
              "\nOur knowledge engineers spent years crafting our complex food ontology, which allows us to " \
              "understand the relationships between ingredients, recipes, nutrition, allergens, and more." \
              "" \
              "\nWe can help you find recipies if you know your ingredients."

    display(message)


def user_ingredients_input():
    # Function to take the ingredients from the user.
    message = '\nEnter the list of ingredients in comma separated format or type "e" in case you don\'t wish to ' \
              'continue ' \
              'today \nFor example - apple, eggs, wheat-bread: '
    input_args = [item for item in input(message).split(', ')]
    return input_args


def user_like_input():
    # Function to take the user input in case they like the recipe.
    message = '\nDo you like this recipe? Type "y" if you like the recipe: '
    input_args = input(message)
    return input_args


def user_menu_input():
    # Function to take the user's choice from the menu.
    input_args = input()
    return input_args


def display_processing_message(params) -> None:
    # Function to display the processing message when the recipes are being fetched.
    message: str = "Ingredients:\n"
    for i in range(len(params)):
        message += params[i]
        if i < len(params) - 1:
            message += ', '
    message += "\nSearching for recipies based on the ingredient/s you entered..."
    display(message, '')


def display_menu() -> None:
    # Function to display the Menu.
    message = "Select an option from the Menu by typing the appropriate letter" \
              "\nn:Next Recipe \ns:Display Shopping Cart \nr:New Ingredients \ne:Exit:"

    display(message)


def display_list_empty() -> None:
    # Function to display the message when no more recipes left.
    message = "No more recipes left"
    display(message)


def display_recipe(data):
    # Function to display the recipe with the title and instructions.
    message = "\n\nRecipe:" \
              "{}".format(data['name'])
    message += "\n\nInstructions:" \
               "{}".format(data['instructions'])
    display(message)


def display_missing_ingredients(data):
    # Function to display the list of missing ingredients.
    message = "\n\nRecipe Name:" \
              "{}".format(data['name'])
    message += "\nMissing Ingredients:" \
               "\n{col1: >50} {col2: >50} {col3: >50}".format(col1="Ingredient", col2="Amount", col3="Aisle")
    for row in data['missedIngredients']:
        message += "\n{: >50} {: >50} {: >50}".format(row['name'], row['amount'], row['aisle'])
    display(message)


def display_shopping_cart(data, total_cost):
    # Function to display the shopping cart with the list of items and estimated cost.
    message = "\nShopping List:" \
               "\n{col1: >40} {col2: >40} {col3: >40} {col4: >40}".format(col1="Ingredient", col2="Amount",
                                                                          col3="Cost (in cents)", col4="Aisle")
    for key, val in data.items():
        message += "\n{: >40} {: >40} {: >40} {: >40}".format(val['item'], val['amount'], val['cost']['value'],
                                                              val['aisle'])
    message += '\n\n{col1: >40} {col2: >81}'.format(col1="Total Estimated Cost (in $)", col2=total_cost)
    display(message)


def display_error_message(error_obj) -> None:
    # Function to display the error messages.
    message = "\n\nLooks like we ran into a problem. Please check below for the description and next set of actions"
    message += "\nIssue: {}".format(error_obj['error_message'])
    display(message)


def display_exit_message() -> None:
    # Function to display the exit message.
    message = "Thank you for using Spoonacular." \
              "\nHope you had a wonderful experience. Have a good one!"

    display(message)


def display(message, separator='\n') -> None:
    print(message, end=separator)
