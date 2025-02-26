from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("""
# Project
Hello *world!*
""")

# Load datasets
def load_data():
    resale_list = [
        pd.read_csv("ResaleFlatPricesBasedonApprovalDate19901999.csv"),
        pd.read_csv("ResaleFlatPricesBasedonApprovalDate2000Feb2012.csv"),
        pd.read_csv("ResaleFlatPricesBasedonRegistrationDateFromMar2012toDec2014.csv"),
        pd.read_csv("ResaleFlatPricesBasedonRegistrationDateFromJan2015toDec2016.csv"),
        pd.read_csv("ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv"),
    ]
    resale = pd.concat(resale_list, ignore_index=True)
    # 2015年以前的数据没有剩余租约
    resale.insert(0, "year", resale["month"].str.split('-').str[0], True)
    resale['remaining_lease'] = (99 + resale['lease_commence_date'].astype(int)) - resale['year'].astype(int)

    rental = pd.read_csv("renting.csv")

    return resale, rental

# Add an option to filter based on time and an option to filter as resale or rental dataset
# def add_filter_options():
#     resale, rental = load_data()
#
#     # Sidebar for dataset selection
#     dataset_choice = st.sidebar.radio("Choose the dataset", ('Resale', 'Rental'))
#
#     if dataset_choice == 'Resale':
#         st.title("Resale Dataset")
#         st.header('Time Filter')
#         min_date = datetime(1990, 1, 1)
#         max_date = datetime.now()
#         start_date = st.date_input("Choose Start Date", min_value=min_date, max_value=max_date, value=min_date,
#                                    key="resale_start")
#         end_date = st.date_input("Choose End Date", min_value=min_date, value=max_date, key="resale_end")
#
#         if st.button("Search", key="resale"):
#             # 根据选择的日期范围过滤数据集
#             resale = resale[
#                 (resale['month'] >= start_date.strftime("%Y-%m")) & (resale['month'] <= end_date.strftime("%Y-%m"))]
#
#         st.write(resale)
#
#         resale['price_per_sqm'] = resale.resale_price / resale.floor_area_sqm
#         st.header("data statistics and visualization")
#         st.subheader('mean of resale_price_per_sqm according to time')
#         resale1 = resale[['month', 'price_per_sqm']]
#         resale2 = resale1.groupby('month').agg('mean')
#         resale3 = resale1.groupby('month').agg('median')
#
#         st.write(resale2)
#         st.subheader('trend of resale_price_per_sqm according to time')
#
#         fig, ax = plt.subplots(figsize=(10, 5))
#         ax.plot(resale2['price_per_sqm'].index, resale2['price_per_sqm'], 'r--', label='mean')
#         ax.plot(resale3['price_per_sqm'].index, resale3['price_per_sqm'], 'g--', label='media')
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('mean and medium of resale_price_per_sqm according to time')
#         plt.xlabel("time")
#         plt.ylabel('mean and medium of resale_price_per_sqm')
#         plt.legend()
#         st.pyplot(fig)
#
#         st.subheader('trend of resale number according to time')
#         resale4 = resale1.groupby('month').agg('count')
#
#         fig2, ax = plt.subplots(figsize=(10, 5))
#         ax.plot(resale4['price_per_sqm'].index, resale2['price_per_sqm'], 'r--', label='count')
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('number of resale in a month according to time')
#         plt.xlabel("time")
#         plt.ylabel('number of resale in a month')
#         plt.legend()
#         st.pyplot(fig2)
#
#         resale11 = resale[['town', 'price_per_sqm']]
#         resale4 = resale11.groupby('town').agg('count')
#         resale41 = resale4.sort_values(by='price_per_sqm', ascending=False, inplace=False)
#         resale41.columns = ['number of transactions']
#
#         st.subheader('popular neighborhood')
#         st.write(resale41)
#         st.subheader('number of resales according to town')
#
#         fig3, ax = plt.subplots(figsize=(14, 5))
#         ax.bar(range(len(resale4)), resale4['price_per_sqm'], tick_label=resale4.index)
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('number of resales according to town')
#         plt.xlabel("town")
#         plt.ylabel('number or resales')
#         st.pyplot(fig3)
#
#         st.subheader('mean resale_price_per_sqm according to town')
#
#         fig4, ax = plt.subplots(figsize=(14, 5))
#         resale5 = resale11.groupby('town').agg('mean')
#         ax.bar(range(len(resale5)), resale5['price_per_sqm'], tick_label=resale4.index)
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('mean resale_price_per_sqm according to town')
#         plt.xlabel("town")
#         plt.ylabel('mean resale_price_per_sqm')
#         st.pyplot(fig4)
#
#
#     elif dataset_choice == 'Rental':
#         st.title("Rental Dataset")
#         st.header('Time Filter')
#         rental_start_date = st.date_input("Choose Start Date", min_value=datetime(2021, 1, 1), max_value=datetime.now(),
#                                           value=datetime(2021, 1, 1), key="rental_start")
#         rental_end_date = st.date_input("Choose End Date", min_value=datetime(2021, 1, 1), value=datetime.now(),
#                                         key="rental_end")
#
#         if st.button("Search"):
#             # 根据选择的日期范围过滤数据集
#             rental = rental[
#                 (rental['rent_approval_date'] >= rental_start_date.strftime("%Y-%m")) & (
#                             rental['rent_approval_date'] <= rental_end_date.strftime("%Y-%m"))]
#
#
#         st.write(rental)
#
#         st.header("data statistics and visualization")
#         st.subheader('mean of rental price according to time')
#         resale = rental
#         resale1 = resale[['rent_approval_date', 'monthly_rent']]
#         resale2 = resale1.groupby('rent_approval_date').agg('mean')
#         resale3 = resale1.groupby('rent_approval_date').agg('median')
#
#         st.write(resale2)
#         st.subheader('trend of rental price according to time')
#
#         fig, ax = plt.subplots(figsize=(10, 5))
#         ax.plot(resale2['monthly_rent'].index, resale2['monthly_rent'], 'r--', label='mean')
#         ax.plot(resale3['monthly_rent'].index, resale3['monthly_rent'], 'g--', label='media')
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('mean and medium of rental price according to time')
#         plt.xlabel("time")
#         plt.ylabel('mean and medium of rental price')
#         plt.legend()
#         st.pyplot(fig)
#
#         st.subheader('trend of rental number according to time')
#         resale4 = resale1.groupby('rent_approval_date').agg('count')
#
#         fig2, ax = plt.subplots(figsize=(10, 5))
#         ax.plot(resale4['monthly_rent'].index, resale2['monthly_rent'], 'r--', label='count')
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('number of rentals in a month according to time')
#         plt.xlabel("time")
#         plt.ylabel('number of rentals in a month')
#         plt.legend()
#         st.pyplot(fig2)
#
#         resale11 = resale[['town', 'monthly_rent']]
#         resale4 = resale11.groupby('town').agg('count')
#         resale41 = resale4.sort_values(by = 'monthly_rent',ascending = False, inplace = False)
#         resale41.columns = ['number of transactions']
#
#         st.subheader(' neighborhood')
#         st.write(resale41)
#         st.subheader('number of rentals according to town')
#
#         fig3, ax = plt.subplots(figsize=(14, 5))
#         ax.bar(range(len(resale4)), resale4['monthly_rent'], tick_label=resale4.index)
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('number of rentals according to town')
#         plt.xlabel("town")
#         plt.ylabel('number or rentals')
#         st.pyplot(fig3)
#
#         st.subheader('mean rental price according to town')
#
#         fig4, ax = plt.subplots(figsize=(14, 5))
#         resale5 = resale11.groupby('town').agg('mean')
#         ax.bar(range(len(resale5)), resale5['monthly_rent'], tick_label=resale4.index)
#         for tick in ax.get_xticklabels():
#             tick.set_rotation(30)
#         plt.title('mean rental price according to town')
#         plt.xlabel("town")
#         plt.ylabel('mean rental price')
#         st.pyplot(fig4)

def time_filter(label, dataset):

    st.title("%s DataSet" %label)
    st.header('Time Filter')
    if label == 'Resale':
        min_date = datetime(1990, 1, 1)
    else:
        min_date = datetime(2021, 1, 1)
    max_date = datetime.now()

    start_date = st.date_input("Choose Start Date", min_value=min_date, max_value=max_date, value=min_date,
                                   key="start_date")
    end_date = st.date_input("Choose End Date", min_value=min_date, value=max_date, key="end_date")

    st.button("Search")
     # 根据选择的日期范围过滤数据集
    if label == 'Resale':
        dataset = dataset[
            (dataset['month'] >= start_date.strftime("%Y-%m")) & (dataset['month'] <= end_date.strftime("%Y-%m"))]
    else:
        dataset = dataset[
            (dataset['rent_approval_date'] >= start_date.strftime("%Y-%m")) & (
                    dataset['rent_approval_date'] <= end_date.strftime("%Y-%m"))]


    st.write(dataset)
    return dataset

def filter_by_category(resale, rental):
    label = st.sidebar.radio("Choose the dataset", ('Resale', 'Rental'))
    if label == "Resale":
        return label, resale
    else:
        return label, rental
