import pandas as pd
import streamlit as st
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import logging
from streamlit_option_menu import option_menu


def app():
    
    st.title("NetCDF (Altitude)")
    "## KeplerGL"
    map_style = eval(open("mapconfig_pre.json").read())
    sess = Session.builder.configs(st.secrets["geo-hackathon"]).create()
    st.markdown("This vizualization uses XXX-precipitation_accumulation-PT01H.nc files.", unsafe_allow_html=True)
    #st.markdown("The width of hexagons visualizes the population density. For more details click legend icon.", unsafe_allow_html=True)
    spatialfeatures = sess.table('METOFFICE.HACKATHON.precipitation_accumulation_h3').select(col("altitude"),  col("GEOID"))
    logging.info('CUSTOM LOG: SnowPark DF is there')
    df = pd.DataFrame(spatialfeatures.collect())
    logging.info('CUSTOM LOG: Pandas df is there')
    map = KeplerGl(config = map_style)
    map.add_data(data=df, name="data")
    keplergl_static(map, height = 600, width = 900, )