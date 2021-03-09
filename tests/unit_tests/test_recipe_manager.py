from core.shopping_manager.classes.recipe_manager import RecipeManager


def test_get_all_recipes_list():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_all_recipes(['apple', 'banana'])
    assert recipes['status'], "Status needs to be true"


def test_get_all_recipes_single_value():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_all_recipes(['apple'])
    assert recipes['status'], "Status needs to be true"


def test_get_all_recipes_symbols():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_all_recipes(['$%'])
    assert recipes['error_code'] == 2001, "No error other than 2001"


def test_get_all_recipes_empty():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_all_recipes([])
    assert recipes['error_code'] == 2001, "No error other than 2001"


def test_get_recipe_single_id():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_recipe(621189)
    assert recipes['status'], "Status needs to be true"


def test_get_recipe_symbols():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_recipe('%@#')
    assert not recipes['status'], "Status needs to be true"


def test_get_recipe_string():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_recipe('219392')
    assert not recipes['status'], "Status needs to be true"


def test_get_ingredient():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_ingredient({'id': 10218, 'amount': 1.0})
    assert recipes['status'], "Status needs to be true"


def test_get_ingredient_string():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_ingredient('test')
    assert not recipes['status'], "Status needs to be true"


def test_get_ingredient_symbols():
    recipe_obj = RecipeManager()
    recipes = recipe_obj.get_ingredient('12#!@')
    assert not recipes['status'], "Status needs to be true"
