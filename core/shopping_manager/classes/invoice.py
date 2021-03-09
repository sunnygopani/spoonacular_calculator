from core.helpers.spoonacular_logger import Logger


# Import the required modules


class Invoice:
    # Invoice maintains the list of liked missing ingredients so far and computes the total estimated cost.

    def __init__(self):
        # Initialize the shopping list, total cost and the logging handler
        self.final_shopping_list = dict()
        self.total_cost = 0
        self.log_object = Logger()
        self.log_handler = self.log_object.get_logger()

    def add_items(self, ingredient_obj={}):
        # Function to add the items to the shopping list and calculate the total estimated cost of the liked recipes.
        # ingredient_obj is a dictionary that includes the cost and unit of each item.
        # example: {
        #           '19719': {
        #                       'item':'apricot jam',
        #                       'amount': 1.0,
        #                       'aisle':'Nut butters, Jams, and Honey',
        #                       'cost':{
        #                               'value':1.25,
        #                               'unit': 'US Cents'
        #                               }
        #                       }
        #          }
        try:
            self.log_handler.debug('Ingredient Object: {}'.format(ingredient_obj))
            ingredient_id = ingredient_obj['id']
            del ingredient_obj['id']
            ingredient = {ingredient_id: ingredient_obj}
            for k, v in ingredient.items():
                v['cost']['value'] = 0.0 if not v['cost']['value'] else v['cost']['value']
                if k not in self.final_shopping_list.keys():
                    self.final_shopping_list[k] = v
                    if v['cost']['unit'] == 'US Cents':
                        self.total_cost += v['cost']['value'] * 0.01
                    else:
                        self.total_cost += v['cost']['value']
                else:
                    self.final_shopping_list[k]['amount'] = self.final_shopping_list.get(k, 0).get('amount', 0) \
                                                            + v['amount']
                    self.final_shopping_list[k]['cost']['value'] = \
                        self.final_shopping_list.get(k, 0).get('cost', 0).get('value', 0) + v['cost']['value']
                    if v['cost']['unit'] == 'US Cents':
                        self.total_cost += v['cost']['value'] * 0.01
                    else:
                        self.total_cost += v['cost']['value']
            self.total_cost = round(self.total_cost, 2)
        except Exception as ex:
            raise str(ex)
