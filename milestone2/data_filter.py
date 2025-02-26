from datetime import datetime
import streamlit as st


def time_filter(label, dataset):
    st.title("_%s Management_" % label)
    st.header('_Time Filter_',divider='rainbow')
    if label == 'Resale':
        min_date = datetime(1990, 1, 1)
    else:
        min_date = datetime(2021, 1, 1)
    max_date = datetime.now()

    start_date = st.date_input("Choose Start Date", min_value=min_date, max_value=max_date, value=min_date,
                               key="start_date")
    end_date = st.date_input("Choose End Date", min_value=min_date, value=max_date, key="end_date")
    if st.button("Search", key='search'):
        # Filter the dataset based on the selected date range.
        if label == 'Resale':
            dataset = dataset[
                (dataset['month'] >= start_date.strftime("%Y-%m")) & (dataset['month'] <= end_date.strftime("%Y-%m"))]
        else:
            dataset = dataset[
                (dataset['rent_approval_date'] >= start_date.strftime("%Y-%m")) & (
                        dataset['rent_approval_date'] <= end_date.strftime("%Y-%m"))]

    return dataset


def filter_by_category(resale, rental):
    label = st.radio("Choose the dataset", ('Resale', 'Rental'))
    if label == "Resale":
        return label, resale
    else:
        return label, rental
