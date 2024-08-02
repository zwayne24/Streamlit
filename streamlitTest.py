import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

# def run_script():
#     os.system('python Self_Service_data_pull.py')

st.set_page_config(layout="wide")

st.title('First Watch Report')

df = pd.read_excel('output.xlsx')

blankIndex = df[df.isnull().all(1)].index[0]


df1 = pd.read_excel('output.xlsx', skiprows= lambda x: x not in range(blankIndex+1))

# if st.button('Update Data'):
#     run_script()
    
#get unique brands as a selectbox
brands = df1['Unnamed: 1'].unique()
brand = st.multiselect('Select Brand', brands)

if st.button('Get Analysis'):
    # Insert containers separated into tabs:
    tabs = ["Total Revenue", "AOV", "Number of Transactions", "Visits", "Panel Visits"]
    tabslist = st.tabs(tabs)    

    for i in range(len(tabs)):
        with tabslist[i]:
            title = tabs[i]
            # import data output.xslx
            df = pd.read_excel('output.xlsx', sheet_name=title)

            blankIndex = df[df.isnull().all(1)].index[0]


            df1 = pd.read_excel('output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+1))
            df2 = pd.read_excel('output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+2, df.shape[0]+1))
            df1 = df1.rename(columns={'Unnamed: 1': 'Brand Name'})      
            df1.set_index(['Brand Name'], inplace=True)
            df2 = df2.rename(columns={'Unnamed: 1': 'Brand Name'})
            df2.set_index(['Brand Name'], inplace=True)
            
            # remove category column
            df1 = df1.iloc[:, 1:]
            df2 = df2.iloc[:, 1:]
            
            # drop rows where Brand Name is not in brand
            if len(brand) > 0:
                df1 = df1[df1.index.get_level_values('Brand Name').isin(brand)]
                df2 = df2[df2.index.get_level_values('Brand Name').isin(brand)]

            # index = first two columns
            to_drop = None
            # change anything datetime to string including headers 
            for col in range(len(df1.columns)):
                if isinstance(df1.columns[col], datetime.date):
                    df1 = df1.rename(columns={df1.columns[col]: df1.columns[col].strftime('%m/%d/%Y')})
            for col in range(len(df2.columns)):
                if isinstance(df2.columns[col], datetime.date):      
                    df2 = df2.rename(columns={df2.columns[col]: df2.columns[col].strftime('%m/%d/%Y')})
                elif 'Unnamed' in df2.columns[col]: 
                    to_drop = col
                    break

            # drop columns from to_drop onwards
            df2 = df2.iloc[:, :to_drop]
            
            styled_df2 = df2.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.0%}")
            
            # remove category column
            df1 = df1.iloc[:, 1:]
            df2 = df2.iloc[:, 1:]
        
            # making the charts
            fig1 = px.line(df1.T)
            fig1.update_yaxes(title_text='')

            fig2 = px.line(df2.T)
            fig2.update_yaxes(title_text='')
        
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)
            
            # display the two dfs
            with st.expander(title):
                st.write(df1)

            with st.expander('Full Data - Yoy Growth %'):
                st.dataframe(styled_df2)

