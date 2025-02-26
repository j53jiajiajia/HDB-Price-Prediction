from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def statistics_resale(resale):
    resale['price_per_sqm'] = resale.resale_price / resale.floor_area_sqm
    # st.header("Data Statistics and Visualization")
    st.subheader('Trend of Resale Price(per sqm) Over Years')
    resale1 = resale[['month', 'price_per_sqm']]
    resale2 = resale1.groupby('month').agg('mean')
    resale3 = resale1.groupby('month').agg('median')

    # st.write(resale2)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(pd.to_datetime(resale2['price_per_sqm'].index), resale2['price_per_sqm'], 'r--', label='mean')
    ax.plot(pd.to_datetime(resale3['price_per_sqm'].index), resale3['price_per_sqm'], 'g--', label='media')
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('Unit Resale Price Over Years')
    plt.xlabel("Years")
    plt.ylabel('Unit Resale Price')
    plt.legend()
    st.pyplot(fig)

    st.subheader('Trend of Transactions Over Years')
    resale4 = resale1.groupby('month').agg('count')

    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(pd.to_datetime(resale4['price_per_sqm'].index), resale4['price_per_sqm'], 'r--', label='count')
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('number of resale in a month according to time')
    plt.xlabel("Years")
    plt.ylabel('Number of Transactions')
    plt.legend()
    st.pyplot(fig2)

    resale11 = resale[['town', 'price_per_sqm']]
    resale4 = resale11.groupby('town').agg('count')
    resale41 = resale4.sort_values(by='price_per_sqm', ascending=False, inplace=False)
    resale41.columns = ['number of transactions']

    st.subheader('Popular Neighborhood')
    # st.write(resale41)

    fig3, ax = plt.subplots(figsize=(14, 5))
    ax.bar(range(len(resale4)), resale4['price_per_sqm'], tick_label=resale4.index)
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('number of resales according to town')
    plt.xlabel("town")
    plt.ylabel('number or resales')
    st.pyplot(fig3)

    st.subheader('Mean Resale Price(per sqm) against Town')

    fig4, ax = plt.subplots(figsize=(14, 5))
    resale5 = resale11.groupby('town').agg('mean')
    ax.bar(range(len(resale5)), resale5['price_per_sqm'], tick_label=resale4.index)
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('mean resale_price_per_sqm according to town')
    plt.xlabel("town")
    plt.ylabel('mean resale_price_per_sqm')
    st.pyplot(fig4)



def statistics_rental(resale):
    # st.header("Data Statistics and Visualization")
    st.subheader('Average Rental Price over Time')
    resale1 = resale[['rent_approval_date', 'monthly_rent']]
    resale2 = resale1.groupby('rent_approval_date').agg('mean')
    resale3 = resale1.groupby('rent_approval_date').agg('median')

    # st.write(resale2)
    st.subheader('Trend of Rental Price against Time')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(resale2['monthly_rent'].index, resale2['monthly_rent'], 'r--', label='mean')
    ax.plot(resale3['monthly_rent'].index, resale3['monthly_rent'], 'g--', label='media')
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('mean and medium of rental price according to time')
    plt.xlabel("time")
    plt.ylabel('mean and medium of rental price')
    plt.legend()
    st.pyplot(fig)

    st.subheader('Trend of Rental Number against Time')
    resale4 = resale1.groupby('rent_approval_date').agg('count')

    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(resale4['monthly_rent'].index, resale4['monthly_rent'], 'r--', label='count')
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('number of rentals in a month according to time')
    plt.xlabel("time")
    plt.ylabel('number of rentals in a month')
    plt.legend()
    st.pyplot(fig2)

    resale11 = resale[['town', 'monthly_rent']]
    resale4 = resale11.groupby('town').agg('count')
    resale41 = resale4.sort_values(by='monthly_rent', ascending=False, inplace=False)
    resale41.columns = ['number of transactions']

    st.subheader('Popular Neighborhood')
    # st.write(resale41)
    st.subheader('Number of Rentals against Town')

    fig3, ax = plt.subplots(figsize=(14, 5))
    ax.bar(range(len(resale4)), resale4['monthly_rent'], tick_label=resale4.index)
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('number of rentals according to town')
    plt.xlabel("town")
    plt.ylabel('number or rentals')
    st.pyplot(fig3)

    st.subheader('Mean Rental Price against Town')

    fig4, ax = plt.subplots(figsize=(14, 5))
    resale5 = resale11.groupby('town').agg('mean')
    ax.bar(range(len(resale5)), resale5['monthly_rent'], tick_label=resale4.index)
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
    plt.title('mean rental price according to town')
    plt.xlabel("town")
    plt.ylabel('mean rental price')
    st.pyplot(fig4)


def display_statistic(label,resale):
    if label =='Resale':
        statistics_resale(resale)
    else:
        statistics_rental(resale)
