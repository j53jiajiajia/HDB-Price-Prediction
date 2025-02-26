from datetime import datetime
import streamlit as st
import pandas as pd

# Load datasets
def load_data():
    resale_list = [
        pd.read_csv("./data/ResaleFlatPricesBasedonApprovalDate19901999.csv"),
        pd.read_csv("./data/ResaleFlatPricesBasedonApprovalDate2000Feb2012.csv"),
        pd.read_csv("./data/ResaleFlatPricesBasedonRegistrationDateFromMar2012toDec2014.csv"),
        pd.read_csv("./data/ResaleFlatPricesBasedonRegistrationDateFromJan2015toDec2016.csv"),
        pd.read_csv("./data/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv"),
    ]
    resale = pd.concat(resale_list, ignore_index=True)
    # 2015年以前的数据没有剩余租约
    resale.insert(0, "year", resale["month"].str.split('-').str[0], True)
    resale['remaining_lease'] = (99 + resale['lease_commence_date'].astype(int)) - resale['year'].astype(int)

    rental = pd.read_csv("./data/renting.csv")

    return resale, rental


# Clean the resale data by renaming flat_type and flat_model items to avoid capital and - problems
def clean_data(resale):
    resale['flat_type'] = resale['flat_type'].replace('MULTI-GENERATION', 'MULTI GENERATION')
    # print(resale['flat_type'].value_counts())

    flat_model_replace = {'NEW GENERATION': 'New Generation', 'SIMPLIFIED': 'Simplified', 'STANDARD': 'Standard',
                          'MODEL A-MAISONETTE': 'Model A-Maisonette', 'MULTI GENERATION': 'Multi Generation',
                          'IMPROVED-MAISONETTE': 'Improved-Maisonette', '2-ROOM': '2-room', 'MODEL A': 'Model A',
                          'MAISONETTE': 'Maisonette', 'IMPROVED': 'Improved', 'TERRACE': 'Terrace',
                          'PREMIUM APARTMENT': 'Premium Apartment', 'APARTMENT': 'Apartment'}
    resale['flat_model'] = resale['flat_model'].replace(flat_model_replace)
    # print(resale['flat_model'].value_counts())

    # duplicates = resale.duplicated()
    # print(f"Number of duplicate rows: {duplicates.sum()}")
    # --- delete the duplicates (I am not sure if we should do this?) ---
    # resale = resale.drop_duplicates()

    return resale


# Add an option to filter based on time and an option to filter as resale or rental dataset
def add_filter_options():
    resale, rental = load_data()

    resale = clean_data(resale)

    # Sidebar for dataset selection
    dataset_choice = st.sidebar.radio("Choose the dataset", ('Resale', 'Rental'))

    if dataset_choice == 'Resale':
        st.title("Resale Dataset")
        st.header('Time Filter')
        min_date = datetime(1990, 1, 1)
        max_date = datetime.now()
        start_date = st.date_input("Choose Start Date", min_value=min_date, max_value=max_date, value=min_date,
                                   key="resale_start")
        end_date = st.date_input("Choose End Date", min_value=min_date, value=max_date, key="resale_end")

        if st.button("Search", key="resale"):
            # 根据选择的日期范围过滤数据集
            resale = resale[
                (resale['month'] >= start_date.strftime("%Y-%m")) & (resale['month'] <= end_date.strftime("%Y-%m"))]

        st.write(resale)

    elif dataset_choice == 'Rental':
        st.title("Rental Dataset")
        st.header('Time Filter')
        rental_start_date = st.date_input("Choose Start Date", min_value=datetime(2021, 1, 1), max_value=datetime.now(),
                                          value=datetime(2021, 1, 1), key="rental_start")
        rental_end_date = st.date_input("Choose End Date", min_value=datetime(2021, 1, 1), value=datetime.now(),
                                        key="rental_end")

        if st.button("Search", key="rent"):
            # 根据选择的日期范围过滤数据集
            rental = rental[
                (rental['rent_approval_date'] >= rental_start_date.strftime("%Y-%m")) & (
                            rental['rent_approval_date'] <= rental_end_date.strftime("%Y-%m"))]

        st.write(rental)

