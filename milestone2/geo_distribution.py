#!/usr/bin/env python
# coding: utf-8
import folium
import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st


def append_geo_spatial(resale, rental):
    # remove the first column id
    zipcode_mapper = pd.read_csv("data/sg_zipcode_mapper_utf.csv", index_col=0)
    # convert postal as str
    zipcode_mapper['postal'] = zipcode_mapper['postal'].astype('str')
    zipcode_mapper['postal.1'] = zipcode_mapper['postal.1'].astype('str')
    zipcode_mapper_dropped = zipcode_mapper.drop_duplicates(subset=["block", "street_name"])
    # print(len(zipcode_mapper), len(zipcode_mapper_dropped))
    resale_geo = resale.merge(zipcode_mapper_dropped, on=["block", "street_name"], how="left")
    rental_geo = rental.merge(zipcode_mapper_dropped, on=["block", "street_name"], how="left")
    # index's continuity
    resale_geo_dataset = resale_geo.dropna().reset_index(drop=True)
    rental_geo_dataset = rental_geo.dropna().reset_index(drop=True)
    resale_geo_dataset["verbose"], rental_geo_dataset["verbose"] = 1, 1
    # print(len(resale_geo), len(resale_geo_dataset))
    # print(len(rental_geo), len(rental_geo_dataset))
    return resale_geo_dataset, rental_geo_dataset


def display_heatmap(dataset):
    st.subheader('Geospatial Distribution')
    default_location = [1.36, 103.82]
    # if st.checkbox('select to display'):
    m = leafmap.Map(center=default_location, zoom=12)
    m.add_heatmap(dataset, latitude="lat", longitude="lng", value="verbose", name="Heatmap", radius=10)
    m.add_child(folium.LatLngPopup())
    m.to_streamlit()
