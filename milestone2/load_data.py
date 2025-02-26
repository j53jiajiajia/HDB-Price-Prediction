import pandas as pd


def load_data():
    resale_list = [
        pd.read_csv("./data/ResaleFlatPricesBasedonApprovalDate19901999.csv"),
        pd.read_csv("./data/ResaleFlatPricesBasedonApprovalDate2000Feb2012.csv"),
        pd.read_csv("./data/ResaleFlatPricesBasedonRegistrationDateFromMar2012toDec2014.csv"),
        pd.read_csv("./data/ResaleFlatPricesBasedonRegistrationDateFromJan2015toDec2016.csv"),
        pd.read_csv("./data/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv"),
    ]
    resale = pd.concat(resale_list, ignore_index=True)
    rental = pd.read_csv("./data/renting.csv")

    return resale, rental

#
# def read_resale_model():
#     return pd.read_csv("./data/resale_model_dataset.csv")
#
#
# def load_mrt_data():
#     mrt = pd.read_csv("./data/mrt_data.csv")
#     mrt.drop(columns=['type'], inplace=True)
#     return mrt
#
# def load_shopping_malls_data():
#     shopping_malls = pd.read_csv("./data/sg-shopping-malls.csv")
#     return shopping_malls
#
# def load_primary_schools_data():
#     primary_schools = pd.read_csv("./data/sg-primary-schools.csv")
#     return primary_schools
