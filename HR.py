import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px

icon = Image.open("download.png")
st.set_page_config(page_title= "HRM",page_icon=icon, layout= "wide", initial_sidebar_state= "expanded")
st.markdown("<h1 style='text-align: center; color: black;'>Industrial Human Resource Visualization</h1>", unsafe_allow_html=True)

data = pd.read_csv("Final.csv")

selected = option_menu(None, ["Home","Visualization"],
                       icons=["house","bar-chart"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "-2px", "--hover-color": "Black"},
                               "icon": {"font-size": "35px"},
                               "container" : {"max-width": "5000px"},
                               "nav-link-selected": {"background-color": "Black"}})
if selected == "Visualization":
        tab1, tab2, tab3 = st.tabs(["***Main workers***", "***Marginal Workers***","***Main Vs Marginal***" ])
        with tab1:
        
            subtab_1, subtab_2 = st.tabs(["State", "District"])
            with subtab_1:
                unique_states = sorted(data['State'].unique())
                selected_state = st.selectbox("Select State", unique_states)
                state_data = data[data['State'] == selected_state]
                total_main_workers = state_data["MainWorkersTotalPersons"] + state_data["MainWorkersUrbanPersons"] + state_data["MainWorkersRuralPersons"]
                total_state_workers = total_main_workers.sum()
                st.write(f"***Total number of Main workers in {selected_state}: {total_state_workers}***")

                state_gender_totals = data.groupby('State').agg({
                "MainWorkersTotalMales": "sum",
                "MainWorkersUrbanMales": "sum",
                "MainWorkersRuralMales": "sum",
                "MainWorkersTotalFemales": "sum",
                "MainWorkersUrbanFemales": "sum",
                "MainWorkersRuralFemales": "sum"
                }).reset_index()
                state_gender_totals['TotalMaleWorkers'] = (
                state_gender_totals["MainWorkersTotalMales"] + state_gender_totals["MainWorkersUrbanMales"] + state_gender_totals["MainWorkersRuralMales"]
                )
                state_gender_totals['TotalFemaleWorkers'] = (
                state_gender_totals["MainWorkersTotalFemales"] + state_gender_totals["MainWorkersUrbanFemales"] + state_gender_totals["MainWorkersRuralFemales"]
                )
                state_gender_totals['TotalWorkers'] = state_gender_totals['TotalMaleWorkers'] + state_gender_totals['TotalFemaleWorkers']
                state_gender_totals['MalePercentage'] = state_gender_totals['TotalMaleWorkers'] / state_gender_totals['TotalWorkers'] * 100
                state_gender_totals['FemalePercentage'] = state_gender_totals['TotalFemaleWorkers'] / state_gender_totals['TotalWorkers'] * 100
                state_gender_data = state_gender_totals[state_gender_totals['State'] == selected_state].iloc[0]
                labels = ['Male Workers', 'Female Workers']
                values = [state_gender_data['MalePercentage'], state_gender_data['FemalePercentage']]
                fig_pie = px.pie(
                names=labels,
                values=values,
                title=f"Male and Female Workers Distribution in {selected_state}",
                labels={'value': 'Percentage', 'variable': 'Gender'},
                color=labels,
                color_discrete_map={'Male Workers': 'blue', 'Female Workers': 'pink'},)
                st.plotly_chart(fig_pie, use_container_width=True)

                

                category_gender_totals = state_data.groupby('Label').agg({
                "MainWorkersTotalMales": "sum",
                "MainWorkersUrbanMales": "sum",
                "MainWorkersRuralMales": "sum",
                "MainWorkersTotalFemales": "sum",
                "MainWorkersUrbanFemales": "sum",
                "MainWorkersRuralFemales": "sum"
                }).reset_index()
                category_gender_totals['TotalMaleWorkers'] = (
                category_gender_totals["MainWorkersTotalMales"] + category_gender_totals["MainWorkersUrbanMales"] + category_gender_totals["MainWorkersRuralMales"]
                )
                category_gender_totals['TotalFemaleWorkers'] = (
                category_gender_totals["MainWorkersTotalFemales"] + category_gender_totals["MainWorkersUrbanFemales"] + category_gender_totals["MainWorkersRuralFemales"]
                )
                st.write(f"### Total Male and Female Workers in Each Category for {selected_state}")
                fig_bar = px.bar(
                category_gender_totals,
                x='Label',
                y=['TotalMaleWorkers', 'TotalFemaleWorkers'],
                title=f"Total Male and Female Workers by Category in {selected_state}",
                labels={'value': 'Number of Workers', 'variable': 'Gender'},
                barmode='group',
                text_auto=True
                )
                fig_bar.update_traces(textposition='outside', textfont=dict(size=12, family='Arial', color='black', weight='bold'))
                st.plotly_chart(fig_bar, use_container_width=True)
                
                total_main_rural_workers = state_data["MainWorkersRuralPersons"].sum()
                total_main_urban_workers = state_data["MainWorkersUrbanPersons"].sum()
                urban_rural_data = {
                    'Area': ['Urban', 'Rural'],
                    'Main Workers': [total_main_urban_workers, total_main_rural_workers]
                }
                urban_rural_df = pd.DataFrame(urban_rural_data)
                fig_pie_urban_rural = px.pie(
                    urban_rural_df,
                    names='Area',
                    values='Main Workers',
                    title=f"Main Workers Distribution (Urban vs Rural) in {selected_state}",
                    labels={'Main Workers': 'Number of Workers', 'Area': 'Area Type'},
                    color='Area',
                    color_discrete_map={'Urban': 'purple', 'Rural': 'lavender'}
                )
                urban_rural_gender_data = {
                    'Area': ['Urban', 'Rural'],
                    'Male Workers': [
                        state_data["MainWorkersUrbanMales"].sum() ,  
                        state_data["MainWorkersRuralMales"].sum(), 
                    ],
                    'Female Workers': [
                        state_data["MainWorkersUrbanFemales"].sum() , 
                        state_data["MainWorkersRuralFemales"].sum(),  
                    ]
                }
                urban_rural_gender_df = pd.DataFrame(urban_rural_gender_data)
                fig_pie_male_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Male Workers',
                    title=f"Male Main Workers Distribution (Urban vs Rural) in {selected_state}",
                    color='Area',
                    color_discrete_map={'Urban': 'green', 'Rural': 'orange'},
                    labels={'Male Workers': 'Number of Workers', 'Area': 'Area Type'}
                )
                fig_pie_female_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Female Workers',
                    title=f"Female Main Workers Distribution (Urban vs Rural) in {selected_state}",
                    color='Area',
                    color_discrete_map={'Urban': 'blue', 'Rural': 'pink'},
                    labels={'Female Workers': 'Number of Workers', 'Area': 'Area Type'}
                )                

                col1,col2,col3=st.columns(3)
                with col1:
                     st.plotly_chart(fig_pie_urban_rural, use_container_width=True)
                with col2:
                     st.plotly_chart(fig_pie_male_workers, use_container_width=True)
                with col3:
                     st.plotly_chart(fig_pie_female_workers, use_container_width=True)
                     

           
            with subtab_2:
                unique_states = sorted(data['State'].unique())
                selected_state = st.selectbox("Select State", unique_states, key="state_selector_unique_dist")
                state_data = data[data['State'] == selected_state]
                filtered_districts = sorted(state_data['District'].unique())
                selected_district = st.selectbox("Select District", filtered_districts, key="district_selector_unique")
                district_data = state_data[state_data['District'] == selected_district]
                total_workers = (
                district_data["MainWorkersTotalPersons"].sum() +
                district_data["MainWorkersUrbanPersons"].sum() +
                district_data["MainWorkersRuralPersons"].sum()
                )
                st.write(f"***Total number of Main workers: {total_workers}***")
                district_totals = state_data.groupby('District').agg({"MainWorkersTotalPersons": "sum","MainWorkersUrbanPersons": "sum","MainWorkersRuralPersons": "sum"}).reset_index()
                district_totals['TotalWorkers'] = (district_totals["MainWorkersTotalPersons"] + district_totals["MainWorkersUrbanPersons"] + district_totals["MainWorkersRuralPersons"])
                fig = px.bar(district_totals, x='District', y='TotalWorkers', text='TotalWorkers')
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

                total_main_workers = district_data["MainWorkersTotalPersons"] + district_data["MainWorkersUrbanPersons"] + district_data["MainWorkersRuralPersons"]
                total_district_workers = total_main_workers.sum()
                district_gender_totals = data.groupby('District').agg({
                "MainWorkersTotalMales": "sum",
                "MainWorkersUrbanMales": "sum",
                "MainWorkersRuralMales": "sum",
                "MainWorkersTotalFemales": "sum",
                "MainWorkersUrbanFemales": "sum",
                "MainWorkersRuralFemales": "sum"
                }).reset_index()
                district_gender_totals['TotalMaleWorkers'] = (
                district_gender_totals["MainWorkersTotalMales"] + district_gender_totals["MainWorkersUrbanMales"] + district_gender_totals["MainWorkersRuralMales"]
                )
                district_gender_totals['TotalFemaleWorkers'] = (
                district_gender_totals["MainWorkersTotalFemales"] + district_gender_totals["MainWorkersUrbanFemales"] + district_gender_totals["MainWorkersRuralFemales"]
                )
                district_gender_totals['TotalWorkers'] = district_gender_totals['TotalMaleWorkers'] + district_gender_totals['TotalFemaleWorkers']
                district_gender_totals['MalePercentage'] = district_gender_totals['TotalMaleWorkers'] / district_gender_totals['TotalWorkers'] * 100
                district_gender_totals['FemalePercentage'] = district_gender_totals['TotalFemaleWorkers'] / district_gender_totals['TotalWorkers'] * 100
                district_gender_data = district_gender_totals[district_gender_totals['District'] == selected_district].iloc[0]
                labels = ['Male Workers', 'Female Workers']
                values = [district_gender_data['MalePercentage'], district_gender_data['FemalePercentage']]
                fig_pie = px.pie(
                names=labels,
                values=values,
                title=f"Male and Female Workers Distribution in {selected_district}",
                labels={'value': 'Percentage', 'variable': 'Gender'},
                color=labels,
                color_discrete_map={'Male Workers': 'blue', 'Female Workers': 'pink'},
                )
                st.plotly_chart(fig_pie, use_container_width=True)

                category_gender_totals = district_data.groupby('Label').agg({
                "MainWorkersTotalMales": "sum",
                "MainWorkersUrbanMales": "sum",
                "MainWorkersRuralMales": "sum",
                "MainWorkersTotalFemales": "sum",
                "MainWorkersUrbanFemales": "sum",
                "MainWorkersRuralFemales": "sum"
                }).reset_index()
                category_gender_totals['TotalMaleWorkers'] = (
                category_gender_totals["MainWorkersTotalMales"] + category_gender_totals["MainWorkersUrbanMales"] + category_gender_totals["MainWorkersRuralMales"]
                )
                category_gender_totals['TotalFemaleWorkers'] = (
                category_gender_totals["MainWorkersTotalFemales"] + category_gender_totals["MainWorkersUrbanFemales"] + category_gender_totals["MainWorkersRuralFemales"]
                )
                st.write(f"### Total Male and Female Workers in Each Category for {selected_district}")
                fig_bar = px.bar(
                category_gender_totals,
                x='Label',
                y=['TotalMaleWorkers', 'TotalFemaleWorkers'],
                title=f"Total Male and Female Workers by Category in {selected_district}",
                labels={'value': 'Number of Workers', 'variable': 'Gender'},
                barmode='group',
                text_auto=True
                )
                fig_bar.update_traces(
                textposition='outside', 
                textfont=dict(size=10, family='Arial', color='black', weight='bold')
                )
                st.plotly_chart(fig_bar, use_container_width=True)

                total_main_rural_workers = district_data["MainWorkersRuralPersons"].sum()
                total_main_urban_workers = district_data["MainWorkersUrbanPersons"].sum()
                urban_rural_data = {
                    'Area': ['Urban', 'Rural'],
                    'Main Workers': [total_main_urban_workers, total_main_rural_workers]
                }
                urban_rural_df = pd.DataFrame(urban_rural_data)
                fig_pie_urban_rural = px.pie(
                    urban_rural_df,
                    names='Area',
                    values='Main Workers',
                    title=f"Main Workers Distribution (Urban vs Rural)",
                    labels={'Main Workers': 'Number of Workers', 'Area': 'Area Type'},
                    color='Area',
                    color_discrete_map={'Urban': 'purple', 'Rural': 'lavender'}
                )
                urban_rural_gender_data = {
                    'Area': ['Urban', 'Rural'],
                    'Male Workers': [
                        district_data["MainWorkersUrbanMales"].sum() ,  
                        district_data["MainWorkersRuralMales"].sum(), 
                    ],
                    'Female Workers': [
                        district_data["MainWorkersUrbanFemales"].sum() , 
                        district_data["MainWorkersRuralFemales"].sum(),  
                    ]
                }
                urban_rural_gender_df = pd.DataFrame(urban_rural_gender_data)
                fig_pie_male_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Male Workers',
                    title=f"Male Main Workers Distribution (Urban vs Rural)",
                    color='Area',
                    color_discrete_map={'Urban': 'green', 'Rural': 'orange'},
                    labels={'Male Workers': 'Number of Workers', 'Area': 'Area Type'}
                )
                fig_pie_female_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Female Workers',
                    title=f"Female Main Workers Distribution (Urban vs Rural)",
                    color='Area',
                    color_discrete_map={'Urban': 'blue', 'Rural': 'pink'},
                    labels={'Female Workers': 'Number of Workers', 'Area': 'Area Type'}
                )                

                col1,col2,col3=st.columns(3)
                with col1:
                     st.plotly_chart(fig_pie_urban_rural, use_container_width=True)
                with col2:
                     st.plotly_chart(fig_pie_male_workers, use_container_width=True)
                with col3:
                     st.plotly_chart(fig_pie_female_workers, use_container_width=True)
       
        with tab2:
        
            subtab_3, subtab_4 = st.tabs(["State", "District"])
            with subtab_3:
                unique_states = sorted(data['State'].unique())
                selected_state = st.selectbox("Select State", unique_states,key='state_selector_unique_mar')
                state_data = data[data['State'] == selected_state]
                total_Marginal_workers = state_data["MarginalWorkersTotalPersons"] + state_data["MarginalWorkersUrbanPersons"] + state_data["MarginalWorkersRuralPersons"]
                total_state_workers = total_Marginal_workers.sum()
                st.write(f"***Total number of Marginal workers in {selected_state}: {total_state_workers}***")

                state_gender_totals = data.groupby('State').agg({
                "MarginalWorkersTotalMales": "sum",
                "MarginalWorkersUrbanMales": "sum",
                "MarginalWorkersRuralMales": "sum",
                "MarginalWorkersTotalFemales": "sum",
                "MarginalWorkersUrbanFemales": "sum",
                "MarginalWorkersRuralFemales": "sum"
                }).reset_index()
                state_gender_totals['TotalMaleWorkers'] = (
                state_gender_totals["MarginalWorkersTotalMales"] + state_gender_totals["MarginalWorkersUrbanMales"] + state_gender_totals["MarginalWorkersRuralMales"]
                )
                state_gender_totals['TotalFemaleWorkers'] = (
                state_gender_totals["MarginalWorkersTotalFemales"] + state_gender_totals["MarginalWorkersUrbanFemales"] + state_gender_totals["MarginalWorkersRuralFemales"]
                )
                state_gender_totals['TotalWorkers'] = state_gender_totals['TotalMaleWorkers'] + state_gender_totals['TotalFemaleWorkers']
                state_gender_totals['MalePercentage'] = state_gender_totals['TotalMaleWorkers'] / state_gender_totals['TotalWorkers'] * 100
                state_gender_totals['FemalePercentage'] = state_gender_totals['TotalFemaleWorkers'] / state_gender_totals['TotalWorkers'] * 100
                state_gender_data = state_gender_totals[state_gender_totals['State'] == selected_state].iloc[0]
                labels = ['Male Workers', 'Female Workers']
                values = [state_gender_data['MalePercentage'], state_gender_data['FemalePercentage']]
                fig_pie = px.pie(
                names=labels,
                values=values,
                title=f"Male and Female Workers Distribution in {selected_state}",
                labels={'value': 'Percentage', 'variable': 'Gender'},
                color=labels,
                color_discrete_map={'Male Workers': 'blue', 'Female Workers': 'pink'},)
                st.plotly_chart(fig_pie, use_container_width=True)

                category_gender_totals = state_data.groupby('Label').agg({
                "MarginalWorkersTotalMales": "sum",
                "MarginalWorkersUrbanMales": "sum",
                "MarginalWorkersRuralMales": "sum",
                "MarginalWorkersTotalFemales": "sum",
                "MarginalWorkersUrbanFemales": "sum",
                "MarginalWorkersRuralFemales": "sum"
                }).reset_index()
                category_gender_totals['TotalMaleWorkers'] = (
                category_gender_totals["MarginalWorkersTotalMales"] + category_gender_totals["MarginalWorkersUrbanMales"] + category_gender_totals["MarginalWorkersRuralMales"]
                )
                category_gender_totals['TotalFemaleWorkers'] = (
                category_gender_totals["MarginalWorkersTotalFemales"] + category_gender_totals["MarginalWorkersUrbanFemales"] + category_gender_totals["MarginalWorkersRuralFemales"]
                )
                st.write(f"### Total Male and Female Workers in Each Category for {selected_state}")
                fig_bar = px.bar(
                category_gender_totals,
                x='Label',
                y=['TotalMaleWorkers', 'TotalFemaleWorkers'],
                title=f"Total Male and Female Workers by Category in {selected_state}",
                labels={'value': 'Number of Workers', 'variable': 'Gender'},
                barmode='group',
                text_auto=True
                )
                fig_bar.update_traces(textposition='outside', textfont=dict(size=12, family='Arial', color='black', weight='bold'))
                st.plotly_chart(fig_bar, use_container_width=True)

                total_Marginal_rural_workers = state_data["MarginalWorkersRuralPersons"].sum()
                total_Marginal_urban_workers = state_data["MarginalWorkersUrbanPersons"].sum()
                urban_rural_data = {
                    'Area': ['Urban', 'Rural'],
                    'Marginal Workers': [total_Marginal_urban_workers, total_Marginal_rural_workers]
                }
                urban_rural_df = pd.DataFrame(urban_rural_data)
                fig_pie_urban_rural = px.pie(
                    urban_rural_df,
                    names='Area',
                    values='Marginal Workers',
                    title=f"Marginal Workers Distribution (Urban vs Rural) ",
                    labels={'Marginal Workers': 'Number of Workers', 'Area': 'Area Type'},
                    color='Area',
                    color_discrete_map={'Urban': 'purple', 'Rural': 'lavender'}
                )
                urban_rural_gender_data = {
                    'Area': ['Urban', 'Rural'],
                    'Male Workers': [
                        state_data["MarginalWorkersUrbanMales"].sum() ,  
                        state_data["MarginalWorkersRuralMales"].sum(), 
                    ],
                    'Female Workers': [
                        state_data["MarginalWorkersUrbanFemales"].sum() , 
                        state_data["MarginalWorkersRuralFemales"].sum(),  
                    ]
                }
                urban_rural_gender_df = pd.DataFrame(urban_rural_gender_data)
                fig_pie_male_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Male Workers',
                    title=f"Male Marginal Workers Distribution (Urban vs Rural)",
                    color='Area',
                    color_discrete_map={'Urban': 'green', 'Rural': 'orange'},
                    labels={'Male Workers': 'Number of Workers', 'Area': 'Area Type'}
                )
                fig_pie_female_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Female Workers',
                    title=f"Female Marginal Workers Distribution (Urban vs Rural)",
                    color='Area',
                    color_discrete_map={'Urban': 'blue', 'Rural': 'pink'},
                    labels={'Female Workers': 'Number of Workers', 'Area': 'Area Type'}
                )                

                col1,col2,col3=st.columns(3)
                with col1:
                     st.plotly_chart(fig_pie_urban_rural, use_container_width=True)
                with col2:
                     st.plotly_chart(fig_pie_male_workers, use_container_width=True)
                with col3:
                     st.plotly_chart(fig_pie_female_workers, use_container_width=True)
           
            with subtab_4:
                unique_states = sorted(data['State'].unique())
                selected_state = st.selectbox("Select State", unique_states, key="state_selector_unique_dist_mar")
                state_data = data[data['State'] == selected_state]
                filtered_districts = sorted(state_data['District'].unique())
                selected_district = st.selectbox("Select District", filtered_districts, key="district_selector_unique_mar")
                district_data = state_data[state_data['District'] == selected_district]
                total_workers = (
                district_data["MarginalWorkersTotalPersons"].sum() +
                district_data["MarginalWorkersUrbanPersons"].sum() +
                district_data["MarginalWorkersRuralPersons"].sum()
                )
                st.write(f"***Total number of Marginal workers: {total_workers}***")
                district_totals = state_data.groupby('District').agg({"MarginalWorkersTotalPersons": "sum","MarginalWorkersUrbanPersons": "sum","MarginalWorkersRuralPersons": "sum"}).reset_index()
                district_totals['TotalWorkers'] = (district_totals["MarginalWorkersTotalPersons"] + district_totals["MarginalWorkersUrbanPersons"] + district_totals["MarginalWorkersRuralPersons"])
                fig = px.bar(district_totals, x='District', y='TotalWorkers', text='TotalWorkers')
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

                total_Marginal_workers = district_data["MarginalWorkersTotalPersons"] + district_data["MarginalWorkersUrbanPersons"] + district_data["MarginalWorkersRuralPersons"]
                total_district_workers = total_Marginal_workers.sum()
                district_gender_totals = data.groupby('District').agg({
                "MarginalWorkersTotalMales": "sum",
                "MarginalWorkersUrbanMales": "sum",
                "MarginalWorkersRuralMales": "sum",
                "MarginalWorkersTotalFemales": "sum",
                "MarginalWorkersUrbanFemales": "sum",
                "MarginalWorkersRuralFemales": "sum"
                }).reset_index()
                district_gender_totals['TotalMaleWorkers'] = (
                district_gender_totals["MarginalWorkersTotalMales"] + district_gender_totals["MarginalWorkersUrbanMales"] + district_gender_totals["MarginalWorkersRuralMales"]
                )
                district_gender_totals['TotalFemaleWorkers'] = (
                district_gender_totals["MarginalWorkersTotalFemales"] + district_gender_totals["MarginalWorkersUrbanFemales"] + district_gender_totals["MarginalWorkersRuralFemales"]
                )
                district_gender_totals['TotalWorkers'] = district_gender_totals['TotalMaleWorkers'] + district_gender_totals['TotalFemaleWorkers']
                district_gender_totals['MalePercentage'] = district_gender_totals['TotalMaleWorkers'] / district_gender_totals['TotalWorkers'] * 100
                district_gender_totals['FemalePercentage'] = district_gender_totals['TotalFemaleWorkers'] / district_gender_totals['TotalWorkers'] * 100
                district_gender_data = district_gender_totals[district_gender_totals['District'] == selected_district].iloc[0]
                labels = ['Male Workers', 'Female Workers']
                values = [district_gender_data['MalePercentage'], district_gender_data['FemalePercentage']]
                fig_pie = px.pie(
                names=labels,
                values=values,
                title=f"Male and Female Workers Distribution in {selected_district}",
                labels={'value': 'Percentage', 'variable': 'Gender'},
                color=labels,
                color_discrete_map={'Male Workers': 'blue', 'Female Workers': 'pink'},
                )
                st.plotly_chart(fig_pie, use_container_width=True)

                category_gender_totals = district_data.groupby('Label').agg({
                "MarginalWorkersTotalMales": "sum",
                "MarginalWorkersUrbanMales": "sum",
                "MarginalWorkersRuralMales": "sum",
                "MarginalWorkersTotalFemales": "sum",
                "MarginalWorkersUrbanFemales": "sum",
                "MarginalWorkersRuralFemales": "sum"
                }).reset_index()
                category_gender_totals['TotalMaleWorkers'] = (
                category_gender_totals["MarginalWorkersTotalMales"] + category_gender_totals["MarginalWorkersUrbanMales"] + category_gender_totals["MarginalWorkersRuralMales"]
                )
                category_gender_totals['TotalFemaleWorkers'] = (
                category_gender_totals["MarginalWorkersTotalFemales"] + category_gender_totals["MarginalWorkersUrbanFemales"] + category_gender_totals["MarginalWorkersRuralFemales"]
                )
                st.write(f"### Total Male and Female Workers in Each Category for {selected_district}")
                fig_bar = px.bar(
                category_gender_totals,
                x='Label',
                y=['TotalMaleWorkers', 'TotalFemaleWorkers'],
                title=f"Total Male and Female Workers by Category in {selected_district}",
                labels={'value': 'Number of Workers', 'variable': 'Gender'},
                barmode='group',
                text_auto=True
                )
                fig_bar.update_traces(
                textposition='outside', 
                textfont=dict(size=10, family='Arial', color='black', weight='bold')
                )
                st.plotly_chart(fig_bar, use_container_width=True)

                total_Marginal_rural_workers = district_data["MarginalWorkersRuralPersons"].sum()
                total_Marginal_urban_workers = district_data["MarginalWorkersUrbanPersons"].sum()
                urban_rural_data = {
                    'Area': ['Urban', 'Rural'],
                    'Marginal Workers': [total_Marginal_urban_workers, total_Marginal_rural_workers]
                }
                urban_rural_df = pd.DataFrame(urban_rural_data)
                fig_pie_urban_rural = px.pie(
                    urban_rural_df,
                    names='Area',
                    values='Marginal Workers',
                    title=f"Marginal Workers Distribution (Urban vs Rural) ",
                    labels={'Marginal Workers': 'Number of Workers', 'Area': 'Area Type'},
                    color='Area',
                    color_discrete_map={'Urban': 'purple', 'Rural': 'lavender'}
                )
                urban_rural_gender_data = {
                    'Area': ['Urban', 'Rural'],
                    'Male Workers': [
                        district_data["MarginalWorkersUrbanMales"].sum() ,  
                        district_data["MarginalWorkersRuralMales"].sum(), 
                    ],
                    'Female Workers': [
                        district_data["MarginalWorkersUrbanFemales"].sum() , 
                        district_data["MarginalWorkersRuralFemales"].sum(),  
                    ]
                }
                urban_rural_gender_df = pd.DataFrame(urban_rural_gender_data)
                fig_pie_male_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Male Workers',
                    title=f"Male Marginal Workers Distribution (Urban vs Rural)",
                    color='Area',
                    color_discrete_map={'Urban': 'green', 'Rural': 'orange'},
                    labels={'Male Workers': 'Number of Workers', 'Area': 'Area Type'}
                )
                fig_pie_female_workers = px.pie(
                    urban_rural_gender_df,
                    names='Area',
                    values='Female Workers',
                    title=f"Female Marginal Workers Distribution (Urban vs Rural)",
                    color='Area',
                    color_discrete_map={'Urban': 'blue', 'Rural': 'pink'},
                    labels={'Female Workers': 'Number of Workers', 'Area': 'Area Type'}
                )                

                col1,col2,col3=st.columns(3)
                with col1:
                     st.plotly_chart(fig_pie_urban_rural, use_container_width=True)
                with col2:
                     st.plotly_chart(fig_pie_male_workers, use_container_width=True)
                with col3:
                     st.plotly_chart(fig_pie_female_workers, use_container_width=True)

        with tab3:
            subtab_5, subtab_6 =st.tabs(["State", "District"])

            with subtab_5:
                unique_states = sorted(data['State'].unique())
                selected_state = st.selectbox("Select State", unique_states,key="Main_vs_marginal")
                state_data = data[data['State'] == selected_state]
                total_main_workers = (
                    state_data["MainWorkersTotalPersons"] +
                    state_data["MainWorkersUrbanPersons"] +
                    state_data["MainWorkersRuralPersons"]
                ).sum()
                total_marginal_workers = (
                    state_data["MarginalWorkersTotalPersons"] +
                    state_data["MarginalWorkersUrbanPersons"] +
                    state_data["MarginalWorkersRuralPersons"]
                ).sum()
                total_workers = total_main_workers + total_marginal_workers
                st.write(f"Total Workers in {selected_state}: {total_workers}")
                comparison_df = pd.DataFrame({
                    "Worker Type": ["Main Workers", "Marginal Workers"],
                    "Total Workers": [total_main_workers, total_marginal_workers]
                })
                fig_comparison_bar = px.bar(
                    comparison_df,
                    x="Worker Type",
                    y="Total Workers",
                    title=f"Comparison of Main and Marginal Workers in {selected_state}",
                    labels={"Total Workers": "Number of Workers", "Worker Type": "Worker Type"},
                    text="Total Workers",
                    color="Worker Type",
                    color_discrete_map={"Main Workers": "blue", "Marginal Workers": "orange"}
                )
                fig_comparison_bar.update_traces(textposition="outside")
                st.plotly_chart(fig_comparison_bar, use_container_width=True)

                total_main_male_workers = (
                    state_data["MainWorkersTotalMales"] +
                    state_data["MainWorkersUrbanMales"] +
                    state_data["MainWorkersRuralMales"]
                ).sum()
                total_marginal_male_workers = (
                    state_data["MarginalWorkersTotalMales"] +
                    state_data["MarginalWorkersUrbanMales"] +
                    state_data["MarginalWorkersRuralMales"]
                ).sum()
                total_main_female_workers = (
                    state_data["MainWorkersTotalFemales"] +
                    state_data["MainWorkersUrbanFemales"] +
                    state_data["MainWorkersRuralFemales"]
                ).sum()
                total_marginal_female_workers = (
                    state_data["MarginalWorkersTotalFemales"] +
                    state_data["MarginalWorkersUrbanFemales"] +
                    state_data["MarginalWorkersRuralFemales"]
                ).sum()
                male_worker_data = pd.DataFrame({
                    "Worker Type": ["Main Male Workers", "Marginal Male Workers"],
                    "Total Workers": [total_main_male_workers, total_marginal_male_workers]
                })
                female_worker_data = pd.DataFrame({
                    "Worker Type": ["Main Female Workers", "Marginal Female Workers"],
                    "Total Workers": [total_main_female_workers, total_marginal_female_workers]
                })
                fig_male_pie = px.pie(
                    male_worker_data,
                    names="Worker Type",
                    values="Total Workers",
                    title=f"Main vs Marginal Male Workers in {selected_state}",
                    color="Worker Type",
                    color_discrete_map={"Main Male Workers": "lightblue", "Marginal Male Workers": "lavender"}
                )
                fig_female_pie = px.pie(
                    female_worker_data,
                    names="Worker Type",
                    values="Total Workers",
                    title=f"Main vs Marginal Female Workers in {selected_state}",
                    color="Worker Type",
                    color_discrete_map={"Main Female Workers": "pink", "Marginal Female Workers": "purple"}
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig_male_pie, use_container_width=True,key="male")
                with col2:
                    st.plotly_chart(fig_female_pie, use_container_width=True,key="female")

                category_worker_data = state_data.groupby('Label').agg({
                    "MainWorkersTotalPersons": "sum",
                    "MainWorkersUrbanPersons": "sum",
                    "MainWorkersRuralPersons": "sum",
                    "MarginalWorkersTotalPersons": "sum",
                    "MarginalWorkersUrbanPersons": "sum",
                    "MarginalWorkersRuralPersons": "sum"
                }).reset_index()
                category_worker_data['TotalMainWorkers'] = (
                    category_worker_data["MainWorkersTotalPersons"] + 
                    category_worker_data["MainWorkersUrbanPersons"] + 
                    category_worker_data["MainWorkersRuralPersons"]
                )
                category_worker_data['TotalMarginalWorkers'] = (
                    category_worker_data["MarginalWorkersTotalPersons"] + 
                    category_worker_data["MarginalWorkersUrbanPersons"] + 
                    category_worker_data["MarginalWorkersRuralPersons"]
                )
                fig_bar = px.bar(
                    category_worker_data,
                    x='Label',  
                    y=['TotalMainWorkers', 'TotalMarginalWorkers'], 
                    title=f"Main vs Marginal Workers by Category in {selected_state}",
                    labels={'value': 'Total Workers', 'variable': 'Worker Type'},
                    barmode='group',  
                    text_auto=True,  
                    color_discrete_map={"TotalMainWorkers": "lightgreen", "TotalMarginalWorkers": "lightcoral"})
                fig_bar.update_layout(
                    xaxis_title="Category",
                    yaxis_title="Number of Workers",
                    barmode='group',
                    xaxis_tickangle=-45  
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with subtab_6:
                    unique_states = sorted(data['State'].unique())
                    selected_state = st.selectbox("Select State", unique_states, key="Main_vs_marginal1")
                    state_data = data[data['State'] == selected_state]
                    unique_districts = sorted(state_data['District'].unique())
                    selected_district = st.selectbox("Select District", unique_districts, key="District")
                    district_data = state_data[state_data['District'] == selected_district]
                    district_worker_comparison = state_data.groupby('District').agg({
                        "MainWorkersTotalPersons": "sum",
                        "MainWorkersUrbanPersons": "sum",
                        "MainWorkersRuralPersons": "sum",
                        "MarginalWorkersTotalPersons": "sum",
                        "MarginalWorkersUrbanPersons": "sum",
                        "MarginalWorkersRuralPersons": "sum"
                    }).reset_index()

                    district_worker_comparison['TotalMainWorkers'] = (
                        district_worker_comparison["MainWorkersTotalPersons"] +
                        district_worker_comparison["MainWorkersUrbanPersons"] +
                        district_worker_comparison["MainWorkersRuralPersons"]
                    )

                    district_worker_comparison['TotalMarginalWorkers'] = (
                        district_worker_comparison["MarginalWorkersTotalPersons"] +
                        district_worker_comparison["MarginalWorkersUrbanPersons"] +
                        district_worker_comparison["MarginalWorkersRuralPersons"]
                    )
                    fig_comparison_bar = px.bar(
                        district_worker_comparison,
                        x='District',
                        y=['TotalMainWorkers', 'TotalMarginalWorkers'],
                        title=f"Comparison of Main and Marginal Workers by District in {selected_state}",
                        labels={'value': 'Total Workers', 'variable': 'Worker Type'},
                        barmode='group',  
                        text_auto=True,  
                        color_discrete_map={"TotalMainWorkers": "lightgreen", "TotalMarginalWorkers": "lightcoral"}
                    )
                    fig_comparison_bar.update_layout(
                        xaxis_title="District",
                        yaxis_title="Number of Workers",
                        xaxis_tickangle=-45  
                    )
                    st.plotly_chart(fig_comparison_bar, use_container_width=True)

                    total_main_male_workers = (
                        district_data["MainWorkersTotalMales"] +
                        district_data["MainWorkersUrbanMales"] +
                        district_data["MainWorkersRuralMales"]
                    ).sum()
                    total_marginal_male_workers = (
                        district_data["MarginalWorkersTotalMales"] +
                        district_data["MarginalWorkersUrbanMales"] +
                        district_data["MarginalWorkersRuralMales"]
                    ).sum()
                    total_main_female_workers = (
                        district_data["MainWorkersTotalFemales"] +
                        district_data["MainWorkersUrbanFemales"] +
                        district_data["MainWorkersRuralFemales"]
                    ).sum()
                    total_marginal_female_workers = (
                        district_data["MarginalWorkersTotalFemales"] +
                        district_data["MarginalWorkersUrbanFemales"] +
                        district_data["MarginalWorkersRuralFemales"]
                    ).sum()
                    male_worker_data = pd.DataFrame({
                        "Worker Type": ["Main Male Workers", "Marginal Male Workers"],
                        "Total Workers": [total_main_male_workers, total_marginal_male_workers]
                    })
                    female_worker_data = pd.DataFrame({
                        "Worker Type": ["Main Female Workers", "Marginal Female Workers"],
                        "Total Workers": [total_main_female_workers, total_marginal_female_workers]
                    })
                    fig_male_pie = px.pie(
                        male_worker_data,
                        names="Worker Type",
                        values="Total Workers",
                        title=f"Main vs Marginal Male Workers in {selected_district}, {selected_state}",
                        color="Worker Type",
                        color_discrete_map={"Main Male Workers": "lightblue", "Marginal Male Workers": "lavender"}
                    )
                    fig_female_pie = px.pie(
                        female_worker_data,
                        names="Worker Type",
                        values="Total Workers",
                        title=f"Main vs Marginal Female Workers in {selected_district}, {selected_state}",
                        color="Worker Type",
                        color_discrete_map={"Main Female Workers": "pink", "Marginal Female Workers": "purple"}
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(fig_male_pie, use_container_width=True, key="male1")
                    with col2:
                        st.plotly_chart(fig_female_pie, use_container_width=True, key="female1")
                    category_worker_data = district_data.groupby('Label').agg({
                        "MainWorkersTotalPersons": "sum",
                        "MainWorkersUrbanPersons": "sum",
                        "MainWorkersRuralPersons": "sum",
                        "MarginalWorkersTotalPersons": "sum",
                        "MarginalWorkersUrbanPersons": "sum",
                        "MarginalWorkersRuralPersons": "sum"
                    }).reset_index()
                    category_worker_data['TotalMainWorkers'] = (
                        category_worker_data["MainWorkersTotalPersons"] + 
                        category_worker_data["MainWorkersUrbanPersons"] + 
                        category_worker_data["MainWorkersRuralPersons"]
                    )
                    category_worker_data['TotalMarginalWorkers'] = (
                        category_worker_data["MarginalWorkersTotalPersons"] + 
                        category_worker_data["MarginalWorkersUrbanPersons"] + 
                        category_worker_data["MarginalWorkersRuralPersons"]
                    )

                    fig_bar = px.bar(
                        category_worker_data,
                        x='Label',  
                        y=['TotalMainWorkers', 'TotalMarginalWorkers'], 
                        title=f"Main vs Marginal Workers by Category in {selected_district}, {selected_state}",
                        labels={'value': 'Total Workers', 'variable': 'Worker Type'},
                        barmode='group',  
                        text_auto=True,  
                        color_discrete_map={"TotalMainWorkers": "lightgreen", "TotalMarginalWorkers": "lightcoral"}
                    )
                    fig_bar.update_layout(
                        xaxis_title="Category",
                        yaxis_title="Number of Workers",
                        barmode='group',
                        xaxis_tickangle=-45  
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)  

if selected == "Home":
    st.write("### Objective:")
    ("***This project aims to update and analyze the industrial classification of the workforce in India. It focuses on main and marginal workers (excluding cultivators and agricultural laborers), categorized by sex, section, division, and class. The goal is to provide accurate and current data to support policymaking, employment planning, and economic development. The project utilizes data exploration, machine learning, and natural language processing to categorize and analyze different sectors, such as manufacturing, retail, agriculture, and others, providing a detailed understanding of workforce distribution across India.***")

    st.write("### Technologies Used:")
    ("***1.Python as the programming language***")
    ("***2.Pandas for data manipulation***")
    ("***3.Matplotlib and Plotly for data visualization***")
    ("***4.Streamlit for web application***")