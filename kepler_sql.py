import pandas as pd
import json
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Polygon, shape
from folium import Map, Marker, GeoJson
import branca.colormap as cm
import geojson
from geojson.feature import *
from geojson import Feature, FeatureCollection
import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from streamlit_folium import folium_static
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import logging
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Streamlit Geospatial", layout="centered")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com
map_style = eval(open("mapconfig.json").read())
sess = Session.builder.configs(st.secrets["geo-playground"]).create()
    #st.markdown("The color visualizes the average yearly precipitation (red: low precipitation, turquoise: high).", unsafe_allow_html=True)
    #st.markdown("The width of hexagons visualizes the population density. For more details click legend icon.", unsafe_allow_html=True)
spatialfeatures = sess.table('spain_features').select(col("POPULATION"),col("year_prec"), col("summer_min"), col("summer_max"), col("GEOID"))
logging.info('CUSTOM LOG: SnowPark DF is there')
df = pd.DataFrame(spatialfeatures.collect())
logging.info('CUSTOM LOG: Pandas df is there')
st.title("Geospatial Data Visualisation")

txt = st.text_area(label = '', value = 'Enter your query here')
st.button('Run query')
map = KeplerGl(config = map_style)
map.add_data(data=df, name="data")
keplergl_static(map, width = 700, )