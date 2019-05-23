import pandas as pd
import numpy as np
import pickle
from scipy import sparse

#inputs should be stored like that from user and then run :
# price = prediction(name, item_condition_id, category_name, brand_name, shipping, item_description)

name = 'Leather Horse Statues'
item_condition_id = 1
# main_category = 'Home/Home Décor/Home Décor Accents'
main_category = 'Home'
sub_category = 'Home Décor'
sub_category2 = 'Home Décor Accents'
brand_name=""
shipping =1
item_description='New with tags. Leather horses. Retail for [rm]'

class prediction:

    def __init__(self, name, item_condition_id, main_category, sub_category, sub_category2,  brand_name, shipping, item_description):
        self.input_user = {}
        with open('/Users/minalshettigar/Projects/Python/Price_Recommendation/src/algo/transformers.pickle', 'rb') as handle:
            self.transformers = pickle.load(handle)
        self.clf = pickle.load(open("/Users/minalshettigar/Projects/Python/Price_Recommendation/src/algo/model.sav", 'rb'))
        self.input_user['name'] = [name]
        self.input_user['item_condition_id'] = [item_condition_id]
        self.input_user['main_category'] = [main_category]
        self.input_user['sub_category'] = [sub_category]
        self.input_user['sub_category2'] = [sub_category2]
        self.input_user['brand_name'] = [brand_name]
        self.input_user['shipping'] = [shipping]
        self.input_user['item_description'] = [item_description]
        print(self.predicted_price())


    def predicted_price(self):
        data = pd.DataFrame.from_dict(self.input_user)
        data = data[['name', 'item_condition_id', 'brand_name', 'shipping', 'item_description', 'main_category', 'sub_category', 'sub_category2']]
        missing_values = {'brand_name': 'missing', 'sub_category': 'None', 'sub_category2': 'None'}
        data = data.fillna(value=missing_values)
        test_dataset = self.conversion_to_sparse_matrix(data)
        predicted_price = self.clf.predict(test_dataset)
        return predicted_price

    def create_sub_categories(self,dataframe):
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

    def conversion_to_sparse_matrix(self,dataset):
        name_mat = self.transformers['name'].transform(dataset['name'])
        main_mat = self.transformers['main_category'].transform(dataset['main_category'])
        sub_mat = self.transformers['sub_category'].transform(dataset['sub_category'])
        sub2_mat = self.transformers['sub_category2'].transform(dataset['sub_category2'])
        descrip_mat = self.transformers['item_description'].transform(dataset['item_description'])
        brand_mat = self.transformers['brand_name'].transform(dataset['brand_name'])
        item_condition_mat = self.transformers['item_condition_id'].transform(dataset['item_condition_id'])
        shipping_mat = self.transformers['shipping'].transform(dataset['shipping'])
        test_dataset = sparse.hstack([brand_mat, main_mat, sub_mat, sub2_mat, name_mat, descrip_mat,
                                      item_condition_mat, shipping_mat]).tocsr()
        return test_dataset

price = prediction(name, item_condition_id, main_category, sub_category, sub_category2, brand_name, shipping, item_description)