import pytest

from app import main


def test_app_list_ingredients():
    ingredients = ['apple', 'banana']
    pytest.raises(ValueError, main, ingredients)
