import pandas as pd
import numpy as np

class Config():
    def __init__(self):
        self.train_data = pd.read_csv("/Users/minalshettigar/Projects/Python/Mercari_Price/train.tsv", delimiter= '\t')
        self.condition = []
        self.shipping = []
        self.brands = []
        self.main_category = []
        self.sub_category = []
        self.sub_category2 = []

    def get_item_condition_choices(self):
        self.condition = self.train_data['item_condition_id'].unique()
        item_condition_choices = [(i, self.condition[i]) for i in range(len(self.condition))]
        return item_condition_choices

    def get_brand_choices(self):
        self.brands = self.train_data['brand_name'].unique()
        brand_choices = [(i, self.brands[i]) for i in range(len(self.brands))]
        return brand_choices

    def get_shipping_choices(self):
        self.shipping = self.train_data['shipping'].unique()
        shipping_choices = [(i, self.shipping[i]) for i in range(len(self.shipping))]
        return shipping_choices

    def create_sub_categories(self, dataframe):
        dataframe['temp'] = dataframe['category_name'].apply(lambda x: str(x).split('/'))
        main_category = []
        sub_category = []
        sub_category2 = []
        for i in dataframe['temp'].values:
            main_category.append(i[0])
            try:
                sub_category.append(i[1])
            except:
                sub_category.append(np.nan)
            try:
                sub_category2.append(i[2])
            except:
                sub_category2.append(np.nan)
        dataframe['main_category'] = main_category
        dataframe['sub_category'] = sub_category
        dataframe['sub_category2'] = sub_category2
        dataframe = dataframe.drop(columns='temp')
        missing_values = {'brand_name': 'missing', 'sub_category': 'None', 'sub_category2': 'None'}
        dataframe = dataframe.fillna(value=missing_values)
        return dataframe

    def get_categories_choices(self):
        self.updated_train = self.create_sub_categories(self.train_data)
        self.main_category = self.updated_train['main_category'].unique()
        self.sub_category = self.updated_train['sub_category'].unique()
        self.sub_category2 = self.updated_train['sub_category2'].unique()
        main_choices = [(i, self.main_category[i]) for i in range(len(self.main_category))]
        sub_choices = [(i, self.sub_category[i]) for i in range(len(self.sub_category))]
        sub_sub_choices = [(i, self.sub_category2[i]) for i in range(len(self.sub_category2))]
        return main_choices, sub_choices, sub_sub_choices

    def get_item_condition(self):
        self.get_item_condition_choices()
        return self.condition
    
    def get_brand(self):
        self.get_brand_choices()
        return self.brands
    
    def get_shipping(self):
        self.get_shipping_choices()
        return self.shipping
    
    def get_main_category(self):
        self.get_categories_choices
        return self.main_category, self.sub_category, self.sub_category2
    
