import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt

icon = Image.open("download.png")
st.set_page_config(page_title= "HRM", page_icon= icon, layout= "wide", initial_sidebar_state= "expanded")
st.markdown("<h1 style='text-align: center; color: black;'>Industrial Human Resource Geo-Visualization</h1>", unsafe_allow_html=True)

data = pd.read_csv("Final.csv")

col1, col2, col3 = st.columns([1,1,1])

selected = option_menu(None, ["Home","Visualization"],
                       icons=["house","bar-chart"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "-2px", "--hover-color": "Red"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "5000px"},
                               "nav-link-selected": {"background-color": "Red"}})
if selected == "Visualization":
        tab1, tab2 = st.tabs(["***Main workers***", "***Marginal Workers***"])
        with tab1:
            unique_states = sorted(data['State'].unique())
            selected_state = st.selectbox("Select State", unique_states, key="state_selector_unique")
            state_data = data[(data['State'] == selected_state)]
            total_main_workers=state_data["MainWorkersTotalPersons"]+state_data["MainWorkersUrbanPersons"]+state_data["MainWorkersRuralPersons"]
            total_state_workers = total_main_workers.sum()
            st.write(f"***Total number of Main workers: {total_state_workers}***")
            filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
            selected_district = st.selectbox("Select District", filtered_districts, key="district_selector_unique")
            district_data = data[(data['District'] == selected_district)]
            total_workers=district_data["MainWorkersTotalPersons"]+district_data["MainWorkersUrbanPersons"]+district_data["MainWorkersRuralPersons"]
            total_district_workers = total_workers.sum()
            st.write(f"***Total number of district workers: {total_district_workers}***")





