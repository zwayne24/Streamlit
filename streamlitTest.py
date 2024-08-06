import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

st.set_page_config(layout="wide")

st.title('First Watch Report')

df = pd.read_excel('./output.xlsx')

blankIndex = df[df.isnull().all(1)].index[0]


df1 = pd.read_excel('output.xlsx', skiprows= lambda x: x not in range(blankIndex+1))

# Insert containers separated into tabs:
tabs = ["Total Revenue", "AOV", "Number of Transactions", "Visits", "Number of Orders by Income"]
tabslist = st.tabs(tabs + ['Download Raw Data'])    

for i in range(len(tabs)):
    with tabslist[i]:
        if i != len(tabs)-1:
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
            
            # add blank row to row 2 and move everything down
            df_blank_bc = pd.DataFrame(np.nan, index=["BREAKFAST COMPS"], columns=df2.columns)
            df_blank_cd = pd.DataFrame(np.nan, index=["CASUAL DINING COMPS"], columns=df2.columns)
            df2_with_blanks = pd.concat([df2.iloc[:1], df_blank_bc, df2.iloc[1:9], df_blank_cd, df2.iloc[9:]])
            
            styled_df2 = df2_with_blanks.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.0%}")
            
            # create df of just the first row, then the average of rows 2-9, then the average of rows 10-17
            dfAverages = pd.concat([df2_with_blanks.iloc[0], df2_with_blanks.iloc[2:10].mean(), df2_with_blanks.iloc[12:].mean()], axis=1).T
            # index the averages
            dfAverages.index = ['First Watch', 'Breakfast Average', 'Casual Dining Average']
            styled_dfAverages = dfAverages.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.0%}")
            
            # remove category column
            df1 = df1.iloc[:, 1:]
            df2 = df2.iloc[:, 1:]
        
            # making the charts
            fig1 = px.line(df1.T,
                        color_discrete_map={'First Watch': 'black',
                                                df1.index[1]: '#260279',
                                                df1.index[2]: '#31029c',
                                                df1.index[3]: '#1c0159',
                                                df1.index[4]: '#22016d',
                                                df1.index[5]: '#b697ff',
                                                df1.index[6]: '#d3c0ff',
                                                df1.index[7]: '#9362ff',
                                                df1.index[8]: '#a881ff',
                                                df1.index[9]: '#ffea00',
                                                df1.index[10]: '#f7cd00',
                                                df1.index[11]: '#efb000',
                                                df1.index[12]: '#e79300',
                                                df1.index[13]: '#de7500',
                                                df1.index[14]: '#d65800',
                                                df1.index[15]: '#ce3b00',
                                                df1.index[16]: '#c61e00',
                                                df1.index[17]: '#bd0000'})

            fig1.update_traces(line=dict(width=4), selector=dict(name='First Watch'))                                     
            fig1.update_yaxes(title_text='')

            fig2 = px.line(df2.T, 
                        color_discrete_map={'First Watch': 'black',
                                                df1.index[1]: '#260279',
                                                df1.index[2]: '#31029c',
                                                df1.index[3]: '#1c0159',
                                                df1.index[4]: '#22016d',
                                                df1.index[5]: '#b697ff',
                                                df1.index[6]: '#d3c0ff',
                                                df1.index[7]: '#9362ff',
                                                df1.index[8]: '#a881ff',
                                                df1.index[9]: '#ffea00',
                                                df1.index[10]: '#f7cd00',
                                                df1.index[11]: '#efb000',
                                                df1.index[12]: '#e79300',
                                                df1.index[13]: '#de7500',
                                                df1.index[14]: '#d65800',
                                                df1.index[15]: '#ce3b00',
                                                df1.index[16]: '#c61e00',
                                                df1.index[17]: '#bd0000'})
            fig2.update_traces(line=dict(width=4), selector=dict(name='First Watch'))
            fig2.update_yaxes(title_text='')
        
            # add smaller title before the charts
            st.write(f'#### {"Weekly YoY " + title +" Growth"}')
            st.dataframe(styled_df2, height=(df2_with_blanks.shape[0] + 1) * 35 + 3)
            
            with st.expander('Averages'):
                st.dataframe(styled_dfAverages)
            
            st.plotly_chart(fig2)
            st.write(f'#### {"Weekly " + title}')
            st.plotly_chart(fig1)
            
            
            # display the two dfs
            with st.expander(title):
                st.write(df1)        
                
            if i <= 2:
                st.write('Data from Consumer Edge, a panel of credit card transactions')       
            else:
                st.write('Data from Placer.ai, a panel of mobile phone location data') 
                
        else:
            title = tabs[i]
            # import data output.xslx
            df = pd.read_excel('./output.xlsx', sheet_name=title)

            blankIndex = df[df.isnull().all(1)].index[0]

            df1 = pd.read_excel('./output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+1))
            dfYoY = pd.read_excel('./output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+2, df.shape[0]+1))


             # change anything datetime to string including headers 
            for col in range(len(dfYoY.columns)):
                if isinstance(dfYoY.columns[col], datetime.date):
                    dfYoY = dfYoY.rename(columns={dfYoY.columns[col]: dfYoY.columns[col].strftime('%m/%d/%Y')})
                elif 'Unnamed' in dfYoY.columns[col]: 
                    to_drop = col
                    break

            # drop columns from to_drop onwards 
            dfYoY = dfYoY.iloc[:, :to_drop]
            
            # category column = FW for first 7 rows, then Breakfast, then Casual Dining
            dfYoY['Category'] =  ['FW']*7 + ['Breakfast']*7 + ['Casual Dining']*7
            # index is category and Income
            dfYoY.set_index(['Category', 'Income'], inplace=True)
            
            # add blank row to row 2 and move everything down
            dfYoY_blank_bc = pd.DataFrame(np.nan, index=[("BREAKFAST","-")], columns=dfYoY.columns)
            dfYoY_blank_cd = pd.DataFrame(np.nan, index=[("CASUAL DINING","-")], columns=dfYoY.columns)
            dfYOY_with_blanks = pd.concat([dfYoY.iloc[:7], dfYoY_blank_bc, dfYoY.iloc[7:14], dfYoY_blank_cd, dfYoY.iloc[14:]])
            
            styled_dfYoY = dfYOY_with_blanks.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.0%}")
            
            st.write(f'#### {"Weekly YoY Order Volume Growth by Income"}')
            
            st.dataframe(styled_dfYoY, height=(df2_with_blanks.shape[0] + 1) * 35 + 3)
            st.write('Data from Consumer Edge, a panel of credit card transactions')  
            
# add a 'Raw Data" tab where you can download the data
with tabslist[-1]:
    st.write('#### Download Raw Data')
    with open('./output.xlsx', 'rb') as f:
        btn = st.download_button(
             label ='Download',
             data = f, 
             file_name = 'output.xlsx',)