import streamlit as st

from clean_data import clean_data
from data_filter import time_filter, filter_by_category
from data_function import display_statistic
from geo_distribution import append_geo_spatial, display_heatmap
from load_data import load_data

st.set_page_config(page_title="Housing Management", page_icon="🏠")

# loading data
resale, rental = load_data()
# data pre-processing pipeline
resale = clean_data(resale)
resale, rental = append_geo_spatial(resale, rental)

# UI filter
session_state = st.session_state
if 'main_resale_clicked' not in session_state:
    session_state['resale_clicked'] = True

if 'main_rental_clicked' not in session_state:
    session_state['rental_clicked'] = False

if 'main_label' not in session_state:
    session_state['label'] = 'Resale'

with st.sidebar:
    # pick dataset
    st.markdown("## Choose the Dataset as followed:")
    cols = st.columns(3)
    with cols[0]:
        if st.button('Resale'):
            session_state['resale_clicked'] = True
            session_state['rental_clicked'] = False
            session_state['label'] = 'Resale'
    with cols[1]:
        if st.button('Rental', key='rental'):
            session_state['resale_clicked'] = False
            session_state['rental_clicked'] = True
            session_state['label'] = 'Rental'
    if session_state['resale_clicked']:
        st.markdown('<style>.stButton>button {background-color: gray; color: block}</style>', unsafe_allow_html=True)

    if session_state['rental_clicked']:
        st.markdown('<style>.stButton>button {background-color: gray; color: black}</style>', unsafe_allow_html=True)
    # tabs
    st.markdown("## Tabs")
    st.page_link("main.py", label="Statistics", icon="📊")
    st.page_link("pages/prediction.py", label="Prediction", icon="📈")

if session_state['label'] == 'Resale':
    dataset = resale
else:
    dataset = rental
# UI display
dataset = time_filter(session_state['label'], dataset)
data, figures, heatmap = st.tabs(["Data:floppy_disk:", "Figures :bar_chart:", "Heat Map :fire:"])
with data:
    st.write(dataset)
with figures:
    display_statistic(session_state['label'], dataset)
with heatmap:
    display_heatmap(dataset)
