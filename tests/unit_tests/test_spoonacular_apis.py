from core.shopping_manager.libraries.spoonacular_api import SpoonacularApi


def test_search_recipies_by_ingredients_list():
    api_obj = SpoonacularApi()
    recipes = api_obj.search_recipies_by_ingredients({'ingredients': ['apple', 'banana']})
    assert recipes['status'], "Status needs to be true"


def test_search_recipies_by_ingredients_single_value():
    api_obj = SpoonacularApi()
    recipes = api_obj.search_recipies_by_ingredients({'ingredients': ['apple']})
    assert recipes['status'], "Status needs to be true"


def test_search_recipies_by_ingredients_empty():
    api_obj = SpoonacularApi()
    recipes = api_obj.search_recipies_by_ingredients({'ingredients': []})
    assert recipes['error_code'] == 2001, "Raise correct API error"


def test_get_recipe_details_dict():
    api_obj = SpoonacularApi()
    recipe = api_obj.get_recipe_details({'ids': 621189})
    assert recipe['status'], "Status needs to be true"


def test_get_ingredient_details_empty():
    api_obj = SpoonacularApi()
    recipe = api_obj.get_ingredient_details({})
    assert not recipe['status'], "Status needs to be false"


def test_get_ingredient_details():
    api_obj = SpoonacularApi()
    recipe = api_obj.get_ingredient_details({'id': 10218, 'amount': 1.0})
    assert recipe['status'], "Status needs to be true"


def test_http_request_wrong_api_key():
    api_obj = SpoonacularApi({'api_key': '1231241j23'})
    recipe = api_obj.get_ingredient_details({'id': 10218, 'amount': 1.0})
    assert not recipe['status'], "Status needs to be false"
