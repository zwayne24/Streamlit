# imports
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as colors  
import seaborn as sns
import os
import plotly.express as px

# make page wider margins
st.set_page_config(layout="wide")

# title
st.title('First Watch Report')

# Insert containers separated into tabs:
tabs = ["Total Revenue", "AOV", "Number of Transactions", "Visits", "Number of Orders by Income"]
tabslist = st.tabs(tabs + ['Download Raw Data'])    

for i in range(len(tabs)):
    with tabslist[i]:
        if i != len(tabs)-1:
            title = tabs[i]
            # read in excel and find blank row, the excel is set up so the data and YoY % for that data are on the same
            # excel sheet separated by a blank row, so this is to find that blank row and split the data into two dataframes
            df = pd.read_excel('output.xlsx', sheet_name=title)
            blankIndex = df[df.isnull().all(1)].index[0]

            # read in the two dataframes, using skiprows to get the data above and below the blank row
            df1 = pd.read_excel('output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+1))
            df2 = pd.read_excel('output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+2, df.shape[0]+1))
            # rename the first column to Brand Name and set it as the index
            df1 = df1.rename(columns={'Unnamed: 1': 'Brand Name'})      
            df1.set_index(['Brand Name'], inplace=True)
            df2 = df2.rename(columns={'Unnamed: 1': 'Brand Name'})
            df2.set_index(['Brand Name'], inplace=True)
            
            # remove category column
            df1 = df1.iloc[:, 1:]
            df2 = df2.iloc[:, 1:]

            to_drop = None
            # -Change anything datetime to string, including headers. This is to make the headers more readable
            # -Because the overall data has more columns than the YoY data and they're read in off the same sheet
            # we find the first column that has 'Unnamed' in it in the YoY and drop everything after that
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
            
            # Add a blank row to separate the data into First Watch, Breakfast, and Casual Dining
            df_blank_bc = pd.DataFrame(np.nan, index=["BREAKFAST COMPS"], columns=df2.columns)
            df_blank_cd = pd.DataFrame(np.nan, index=["CASUAL DINING COMPS"], columns=df2.columns)
            df2_with_blanks = pd.concat([df2.iloc[:1], df_blank_bc, df2.iloc[1:9], df_blank_cd, df2.iloc[9:]])
            
            # Create heatmap of the data, where 0% is white, negative is red, and positive is green
            divnorm = colors.TwoSlopeNorm(vmin=min(df2.values.min(),-.001), vcenter=0, vmax=max(df2.values.max(),.001))
            styled_df2 = df2_with_blanks.style.background_gradient(cmap="RdYlGn", axis=None, vmin=0, vmax=1, gmap=df2.apply(divnorm)).format("{:.0%}")
            
            # Create a df of the averages for First Watch, Breakfast, and Casual Dining
            dfAverages = pd.concat([df2_with_blanks.iloc[0], df2_with_blanks.iloc[2:10].mean(), df2_with_blanks.iloc[12:].mean()], axis=1).T
            # index the averages
            dfAverages.index = ['First Watch', 'Breakfast Average', 'Casual Dining Average']
            divnorm = colors.TwoSlopeNorm(vmin=min(dfAverages.values.min(),-.001), vcenter=0, vmax=max(dfAverages.values.max(),.001))
            styled_dfAverages = dfAverages.style.background_gradient(cmap="RdYlGn", axis=None, vmin=0, vmax=1, gmap=dfAverages.apply(divnorm)).format("{:.0%}")
        
            # making the line charts. First Watch is always black, then breakfast is purples/blues, casual dining is yellows/reds
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
            # make the First Watch line thicker
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
            # display the YoY heatmap df, set the height
            st.dataframe(styled_df2, height=(df2_with_blanks.shape[0] + 1) * 35 + 8)
            
            # display the averages in a dropdown
            with st.expander('Averages'):
                st.dataframe(styled_dfAverages)
            
            # plot the line charts
            st.plotly_chart(fig2)
            st.write(f'#### {"Weekly " + title}')
            st.plotly_chart(fig1)
            
            # display the full data in a dropdown
            with st.expander(f'{"Weekly " + title}'):
                st.write(df1)        
            
            # site source of data
            if i <= 2:
                st.write('Data from Consumer Edge, a panel of credit card transactions')       
            else:
                st.write('Data from Placer.ai, a panel of mobile phone location data') 
                
        else:
            # for "Number of Orders by Income" tab, repeat data cleaning but with visualizations 
            title = tabs[i]
            df = pd.read_excel('./output.xlsx', sheet_name=title)

            blankIndex = df[df.isnull().all(1)].index[0]

            df1 = pd.read_excel('./output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+1))
            dfYoY = pd.read_excel('./output.xlsx', sheet_name=title, skiprows= lambda x: x not in range(blankIndex+2, df.shape[0]+1))


            for col in range(len(dfYoY.columns)):
                if isinstance(dfYoY.columns[col], datetime.date):
                    dfYoY = dfYoY.rename(columns={dfYoY.columns[col]: dfYoY.columns[col].strftime('%m/%d/%Y')})
                elif 'Unnamed' in dfYoY.columns[col]: 
                    to_drop = col
                    break

            dfYoY = dfYoY.iloc[:, :to_drop]
            
            # add category column: FW for first 7 rows (7 income groups), then Breakfast, then Casual Dining
            dfYoY['Category'] =  ['FW']*7 + ['Breakfast']*7 + ['Casual Dining']*7
            # index is category and Income
            dfYoY.set_index(['Category', 'Income'], inplace=True)
            
            # add blank rows to separate groups
            dfYoY_blank_bc = pd.DataFrame(np.nan, index=[("BREAKFAST","-")], columns=dfYoY.columns)
            dfYoY_blank_cd = pd.DataFrame(np.nan, index=[("CASUAL DINING","-")], columns=dfYoY.columns)
            dfYOY_with_blanks = pd.concat([dfYoY.iloc[:7], dfYoY_blank_bc, dfYoY.iloc[7:14], dfYoY_blank_cd, dfYoY.iloc[14:]])
                        
            divnorm = colors.TwoSlopeNorm(vmin=min(dfYoY.values.min(),-.001), vcenter=0, vmax=max(dfYoY.values.max(),.001))
            styled_dfYoY = dfYOY_with_blanks.style.background_gradient(cmap="RdYlGn", axis=None, vmin=0, vmax=1, gmap=dfYoY.apply(divnorm)).format("{:.0%}")
            
            st.write(f'#### {"Weekly YoY Order Volume Growth by Income"}')
            st.dataframe(styled_dfYoY, height=(dfYOY_with_blanks.shape[0] + 1) * 35 + 8)
            st.write('Data from Consumer Edge, a panel of credit card transactions')  
            
# add a 'Raw Data" tab where you can download the data
with tabslist[-1]:
    st.write('#### Download Raw Data')
    with open('./output.xlsx', 'rb') as f:
        btn = st.download_button(
             label ='Download',
             data = f, 
             file_name = 'output.xlsx',)