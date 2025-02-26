#!/usr/bin/env python
# coding: utf-8
import leafmap.foliumap as leafmap
import pandas as pd


def append_geo_spatial(resale, rental):
    zipcode_mapper = pd.read_csv("data/sg_zipcode_mapper_utf.csv")
    zipcode_mapper_dropped = zipcode_mapper.drop_duplicates(subset=["block", "street_name"])
    print(len(zipcode_mapper), len(zipcode_mapper_dropped))
    resale_geo = resale.merge(zipcode_mapper_dropped, on=["block", "street_name"], how="left")
    rental_geo = rental.merge(zipcode_mapper_dropped, on=["block", "street_name"], how="left")
    resale_geo_dataset = resale_geo.dropna()
    rental_geo_dataset = rental_geo.dropna()
    resale_geo_dataset["verbose"], rental_geo_dataset["verbose"] = 1, 1
    print(len(resale_geo), len(resale_geo_dataset))
    print(len(rental_geo), len(rental_geo_dataset))
    return resale_geo_dataset, rental_geo_dataset


def display_heatmap(dataset):
    m = leafmap.Map(center=[1.36, 103.82], zoom=13)
    m.add_heatmap(dataset, latitude="lat", longitude="lng", value="verbose", name="Heatmap", radius=10)
    m.to_streamlit(height=900)
