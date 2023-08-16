import json
import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Polygon, shape
from folium import Map, Marker, GeoJson
import branca.colormap as cm
import geojson
from geojson.feature import *
from geojson import Feature, FeatureCollection
import streamlit as st
from streamlit_folium import folium_static
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import logging

def dataframe_to_geojson(df_geo, column_name, file_output = None):
    
    '''Produce the GeoJSON for a dataframe that has a geometry column in geojson format already'''
    
    list_features = []
    
    for i,row in df_geo.iterrows():
        feature = Feature(geometry = row["GEOM"], properties = {column_name : row[column_name]})
        list_features.append(feature)
        
    feat_collection = FeatureCollection(list_features)
    
    geojson_result = json.dumps(feat_collection)
    
    #optionally write to file
    if file_output is not None:
        with open(file_output,"w") as f:
            json.dump(feat_collection,f)
    
    return geojson_result


def choropleth_map(df_aggreg, column_name, border_color = 'none', fill_opacity = 0.5, initial_map = None, with_legend = True,
                   kind = "linear"):
    
    
    if initial_map is None:
        initial_map = Map(location= [54.06218540805551, -2.1908748457999665], zoom_start=5, tiles="cartodbpositron")

    geojson_data = dataframe_to_geojson(df_geo = df_aggreg, column_name = column_name)
    
    #plot on map
    name_layer = "Choropleth "
    if kind != "linear":
        name_layer = name_layer + kind
        
    GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': feature['properties'][column_name],
            'color': border_color,
            'weight': 1,
            'fillOpacity': fill_opacity 
        }, 
        name = name_layer
    ).add_to(initial_map)

    return initial_map

def app():

    st.title("Weather forecast")
    sess = Session.builder.configs(st.secrets["geo-hackathon"]).create()
    data = sess.table('forecast').select(col("GEOM"),col("WARNINGLEVEL"))
    logging.info('CUSTOM LOG: SnowPark DF is there')
    df = pd.DataFrame(data.collect())
    logging.info('CUSTOM LOG: Pandas df is there')
    df['GEOM'] = df['GEOM'].apply(lambda x: geojson.loads(x))
    logging.info('CUSTOM LOG: GEOM is done')
    map = choropleth_map(df_aggreg = df, column_name = "WARNINGLEVEL")
    logging.info('CUSTOM LOG: choropleth_map is done')
    folium_static(map)