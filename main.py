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
from apps import forecast, netcdf, precipitations # import your app modules here

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func":forecast.app, "title": "Weather forecast", "icon": "brightness-high-fill"},
    {"func":netcdf.app, "title": "NetCDF (Altitude)", "icon": "grid-3x2"},
    {"func":precipitations.app, "title": "Precipitations", "icon": "cloud-drizzle"}
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Geo examples",
        options=titles,
        icons=icons,
        menu_icon="collection",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        This is a demo app to show the capabilities of Streamlit for geospatial.
    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break