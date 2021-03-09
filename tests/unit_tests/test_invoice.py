import pytest

from core.shopping_manager.classes.invoice import Invoice


def test_add_items_empty():
    inv = Invoice()

    with pytest.raises(Exception):
        assert inv.add_items()


def test_add_items_single_item():
    inv = Invoice()
    inv.add_items({
        'id': 1111,
        'item': 'test_item',
        'amount': 10.0,
        'aisle': 'test aisle',
        'cost': {
            'value': 10.0,
            'unit': 'US Cents'
        }})
    assert inv.total_cost == 0.1, "Total cost must be 10.0"


def test_add_items_same_items():
    inv = Invoice()
    for i in range(2):
        inv.add_items({
            'id': 1111,
            'item': 'test_item',
            'amount': 10.0,
            'aisle': 'test aisle',
            'cost': {
                'value': 10.0,
                'unit': 'US Cents'
            }})
    assert inv.total_cost == 0.2, "Total cost must be 10.0"


def test_add_items_empty_fields():
    inv = Invoice()
    inv.add_items({
        'id': 1111,
        'item': '',
        'amount': '',
        'aisle': '',
        'cost': {
            'value': '',
            'unit': ''
        }
    })
    assert inv.total_cost == 0.0, "Total cost must be 0"
