from core.shopping_manager.classes.invoice import Invoice


def test_add_items_empty():
    inv = Invoice()
    inv.add_items()
    assert inv.total_cost == 0, "Total cost must be 0"


def test_add_items_single_item():
    inv = Invoice()
    inv.add_items({1111: {
        'item': 'test_item',
        'amount': 10.0,
        'aisle': 'test aisle',
        'cost': {
            'value': 10.0,
            'unit': 'ml'
        }
    }})
    assert inv.total_cost == 0.1, "Total cost must be 10.0"


def test_add_items_multiple_items():
    inv = Invoice()
    inv.add_items({1111: {
        'item': 'test_item',
        'amount': 2.0,
        'aisle': 'test aisle',
        'cost': {
            'value': 40,
            'unit': 'ml'
        }
    }, 1112: {
        'item': 'test_item_2',
        'amount': 2,
        'aisle': 'test aisle',
        'cost': {
            'value': 14,
            'unit': 'ml'
        }
    }})
    assert inv.total_cost == 0.54, "Total cost must be 0.54"


def test_add_items_empty_fields():
    inv = Invoice()
    inv.add_items({1111: {
        'item': '',
        'amount': '',
        'aisle': '',
        'cost': {
            'value': '',
            'unit': ''
        }
    }})
    assert inv.total_cost == 0, "Total cost must be 0"
