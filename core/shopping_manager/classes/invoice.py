from core.helpers.spoonacular_logger import Logger


class Invoice:

    def __init__(self):
        self.final_shopping_list = dict()
        self.total_cost = 0
        self.log_object = Logger()
        self.log_handler = self.log_object.get_logger()

    def add_items(self, ingredient_obj):
        try:
            self.log_handler.debug('Ingredient Object: {}'.format(ingredient_obj))
            for k, v in ingredient_obj.items():
                if k not in self.final_shopping_list.keys():
                    self.final_shopping_list[k] = v
                    if v['cost']['unit'] == 'US Cents':
                        self.total_cost += v['cost']['value']*0.01
                    else:
                        self.total_cost += v['cost']['value'] * 0.01
                else:
                    if v['cost']['unit'] == 'US Cents':
                        self.total_cost += v['cost']['value'] * 0.01
                    else:
                        self.total_cost += v['cost']['value'] * 0.01
            self.total_cost = round(self.total_cost, 2)
        except Exception as ex:
            raise ex
