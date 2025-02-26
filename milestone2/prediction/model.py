import os
import pickle

import pandas as pd
from pandas import DataFrame


class ResaleModelCaller:
    def __init__(self):
        self.model = None
        self.cls_model = None
        self.cls_edge = None
        self.ct = None
        self.example_input = DataFrame()


class RentalModelCaller:
    def __init__(self):
        self.model = None
        self.cls_model = None
        self.cls_edge = None
        self.ct = None
        self.example_input = DataFrame()


current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_path, 'model_caller.pkl')
caller_resale: ResaleModelCaller = None
caller_rental: RentalModelCaller = None


def load_prediction_model():
    global caller_resale, caller_rental
    with open(file_path, 'rb') as f:
        caller_resale, caller_rental = pickle.load(f)


def predict_resale(data: DataFrame):
    global caller_resale, caller_rental
    resale_t = caller_resale.ct.transform(data)
    resale_pred = caller_resale.model.predict(resale_t)
    resale_cls_pred_proba = caller_resale.cls_model.predict_proba(resale_t)
    return resale_pred, resale_cls_pred_proba, caller_resale.cls_edge


def predict_rental(data: DataFrame):
    global caller_resale, caller_rental
    rental_t = caller_rental.ct.transform(data)
    rental_pred = caller_rental.model.predict(rental_t)
    rental_cls_pred_proba = caller_rental.cls_model.predict_proba(rental_t)
    return rental_pred, rental_cls_pred_proba, caller_rental.cls_edge


if __name__ == '__main__':
    load_prediction_model()

    print(caller_resale.cls_edge)
    print("=====================================")

    for i in range(2000, 2006):
        data = pd.DataFrame(
            {'year': [str(i)], 'month_category': ['8'], 'flat_type': ['3-ROOM'], 'storey_range': ['11 TO 15'],
             'flat_model': ['Improved'], 'town': ['ANG MO KIO'], 'street_name': ['ANG MO KIO AVE 1'], 'block': ['309']})
        resale_t = caller_resale.ct.transform(data)
        resale_pred = caller_resale.model.predict(resale_t)
        resale_cls_pred = caller_resale.cls_model.predict(resale_t)
        print(f'Resale Prediction: {resale_pred} and {resale_cls_pred}')

    print("=====================================")

    for i in range(1, 6):
        month_inc = i
        month_category = month_inc % 12 + 1
        data = pd.DataFrame(
            {'month_inc': [str(month_inc)], 'month_category': [str(month_category)], 'town': ['ANG MO KIO'],
             'street_name': ['ANG MO KIO AVE 1'], 'block': ['309'], 'flat_type': ['3-ROOM'], })
        rental_t = caller_rental.ct.transform(data)
        rental_pred = caller_rental.model.predict(rental_t)
        rental_cls_pred = caller_rental.cls_model.predict(rental_t)
        print(f'Rental Prediction: {rental_pred} and {rental_cls_pred}')
