import random

import streamlit as st
from clean_data import clean_data
from load_data import load_data
from data_visualization import time_filter, filter_by_category
from geo_distribution import append_geo_spatial, display_heatmap

st.write("""
# Project
Hello *world!*
""")
# loading data
resale, rental = load_data()

# data pre-processing pipeline
clean_data(resale)
resale, rental = append_geo_spatial(resale, rental)

# dataset picker
label, dataset = filter_by_category(resale, rental)

# UI filter
dataset = time_filter(label, dataset)

# UI display
display_heatmap(dataset)
