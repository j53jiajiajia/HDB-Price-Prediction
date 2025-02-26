import math

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer, OneHotEncoder

from trainning.utils import earth_distance
import pickle
import pandas as pd
from pandas import DataFrame
from sklearn.compose import make_column_selector, make_column_transformer

resale_model_dataset = pd.read_csv("./data/resale_model_dataset.csv")

with open('./model/town_classifier.pkl', 'rb') as f:
    town_classifier = pickle.load(f)

with open('./model/distance_regressor.pkl', 'rb') as f:
    mrt_distance_regressor = pickle.load(f)

with open('./model/price_predictor.pkl', 'rb') as f:
    price_preditor = pickle.load(f)

with open('./model/preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

town_classifier.metric = earth_distance
mrt_distance_regressor.metric = earth_distance


def price_predict(lat, lng):
    town = classify_town(lat, lng)
    distance_to_nearest_mrt = cal_distance(lat, lng)
    flat_type = impute_flat_type(town)
    storey_range = impute_storey_range(town, flat_type)

    flat_model = impute_flat_model(town, flat_type)
    sold_year = impute_sold_year(town)
    passed_lease_year = impute_passed_lease_year(town, sold_year)

    data = DataFrame({
        'town': [town],
        'flat_type': [flat_type],
        'storey_range': [storey_range],
        'flat_model': [flat_model],
        'sold_year': [sold_year],
        'passed_lease_date': [int(passed_lease_year)],
        'distance_to_mrt': [float(distance_to_nearest_mrt)]
    })

    data_transformed = preprocessor.transform(data)
    unit_price = price_preditor.predict(data_transformed)
    return unit_price[0]


def cal_distance(lat, lng):
    pos = DataFrame({'lat': [lat], 'lng': [lng]})
    return mrt_distance_regressor.predict(pos)


def classify_town(lat, lng):
    pos = DataFrame({'lat': [lat], 'lng': [lng]})
    return town_classifier.predict(pos)[0]


def impute_flat_type(town: str) -> str:
    flat_type_prob = resale_model_dataset[resale_model_dataset['town'] == town]['flat_type'].value_counts(
        normalize=True)
    return flat_type_prob.idxmax()


def impute_storey_range(town: str, flat_type: str) -> str:
    town_condition = resale_model_dataset['town'] == town
    flat_type_condition = resale_model_dataset['flat_type'] == flat_type
    storey_range_prob = resale_model_dataset[town_condition & flat_type_condition]['storey_range'].value_counts(
        normalize=True)
    return storey_range_prob.idxmax()


def impute_flat_model(town: str, flat_type: str) -> str:
    town_condition = resale_model_dataset['town'] == town
    flat_type_condition = resale_model_dataset['flat_type'] == flat_type
    storey_range_prob = resale_model_dataset[town_condition & flat_type_condition]['flat_model'].value_counts(
        normalize=True)
    return storey_range_prob.idxmax()


def impute_sold_year(town: str) -> str:
    town_subset = resale_model_dataset[resale_model_dataset['town'] == town]
    year = math.floor(town_subset['sold_year'].median())
    return str(year)


def impute_passed_lease_year(town: str, sold_year: str) -> str:
    town_condition = resale_model_dataset['town'] == town
    lease_commence_subset = resale_model_dataset[town_condition]['lease_commence_date']
    lease_commence_year = math.floor(lease_commence_subset.median())
    return str(int(sold_year) - int(lease_commence_year))

# class RentalModelTraining:
#     def __init__(self, df: DataFrame):
#         self.df = df
#         self.init_dataset = df
#         self.rng = np.random.RandomState(42)
#         self.model = None
#
#     def preprocess(self):
#         rental_lr = self.init_dataset[
#             ['rent_approval_date', 'town', 'flat_type', 'block', 'street_name', 'monthly_rent',
#              'postal', 'building', 'verbose', 'lat', 'lng']]
#
#         # year
#         year = rental_lr['rent_approval_date'].apply(lambda x: x.split('-')[0])
#         rental_lr.insert(0, 'year', year)
#         rental_lr['year'] = rental_lr['year'].astype(int)
#         # month
#         month = rental_lr['rent_approval_date'].apply(lambda x: x.split('-')[1])
#         rental_lr.insert(1, 'month', month)
#         rental_lr['month'] = rental_lr['month'].astype(int)
#
#         rental_lr.pop('rent_approval_date')
#         # town
#         ord_enc = preprocessing.OrdinalEncoder(categories='auto')
#         rental_lr['town'] = ord_enc.fit_transform(rental_lr.iloc[:, [2]])
#         # flat_type
#         oh_enc = preprocessing.OneHotEncoder(categories='auto', handle_unknown='ignore')
#         flat_type = oh_enc.fit_transform(rental_lr.iloc[:, [3]])
#         one_hot_feature_names = oh_enc.get_feature_names_out()
#         one_hot_feature_names = [name.replace('-', '_') for name in one_hot_feature_names]
#         oh_df = pd.DataFrame(flat_type.toarray(), columns=one_hot_feature_names)
#         rental_lr = pd.concat([rental_lr, oh_df], axis=1)
#         rental_lr.pop('flat_type')
#         # block
#         rental_lr['block'] = ord_enc.fit_transform(rental_lr.iloc[:, [3]])
#         # street_name
#         rental_lr['street_name'] = ord_enc.fit_transform(rental_lr.iloc[:, [4]])
#         # postal
#         rental_lr['postal'] = rental_lr['postal'].astype(int)
#         # building
#         rental_lr['building'] = ord_enc.fit_transform(rental_lr.iloc[:, [7]])
#         # verbose
#         town_group = rental_lr.groupby('town')
#         town_verbose = town_group['town'].transform('count')
#         rental_lr['verbose'] = town_verbose
#         # mrt
#         nearest_mrt(rental_lr)
#         # monthly_rent
#         price_data = rental_lr.pop('monthly_rent')
#         rental_lr['monthly_rent'] = price_data
#
#         self.df = rental_lr
#
#     def training(self):
#         x = self.df[['year', 'month', 'town', 'block', 'street_name', 'postal', 'building',
#                      'verbose', 'flat_type_1_ROOM', 'flat_type_2_ROOM',
#                      'flat_type_3_ROOM', 'flat_type_4_ROOM', 'flat_type_5_ROOM', 'flat_type_EXECUTIVE', 'nearest_mrt']]
#         y = self.df['monthly_rent']
#         x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=self.rng)
#
#         tree_reg = DecisionTreeRegressor(max_depth=10)
#         tree_reg.fit(x_train, y_train)
#         self.model = tree_reg
#         print("training score:", tree_reg.score(x_train, y_train))
#         print("testing score:", tree_reg.score(x_test, y_test))
#         # 跑了所有的模型，效果都很差，怀疑是数据集数据相关性太强，感觉需要引入额外的数据集合
#
#     def predict(self):
#         pass
