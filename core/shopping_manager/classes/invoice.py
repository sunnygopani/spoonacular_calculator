class Invoice:
    final_shopping_list = dict()
    sum = 0

    def __init__(self):
        pass

    def add_items(self, ingredient_obj):
        for k, v in ingredient_obj.items():
            if k not in self.final_shopping_list.keys():
                self.final_shopping_list[k] = v
                if v['cost']['unit'] == 'US Cents':
                    self.sum = self.sum + (v['cost']['value'] * 0.01)
                else:
                    self.sum = self.sum + (v['cost']['value'])
