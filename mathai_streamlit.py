# -*- coding: utf-8 -*-
"""


@author: joshm


TO RUN: 
    streamlit run week13_streamlit.py

"""



import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
import plotly.figure_factory as ff



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title('Suffolk County Hospitals--Medicare')



    
    
# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  


  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()







hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']

suffolk_hospitals = hospitals_ny[hospitals_ny['county_name'] == 'SUFFOLK']


#Bar Chart
st.subheader('Hospital Ownership - Suffolk County')
bar1 = suffolk_hospitals['hospital_ownership'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('Most hospitals in NY are private voluntary non-profit institutions, followed by government hospitals operated by the state--which includes Stony Brook')


st.subheader('As seen in a PIE Chart:')
fig = px.pie(bar1, values='hospital_ownership', names='index')
st.plotly_chart(fig)

st.subheader('Overall Ratings of Suffolk County Hospitals')
fig = px.bar(suffolk_hospitals, y='hospital_overall_rating', x='hospital_name')
st.plotly_chart(fig)

st.markdown('Stony Brook shares the highest overall hospital rating in Suffolk County with Huntington Hospital')


#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Inpatient data for Stony Brook/Long Island')



inpatient_longisland = df_inpatient_2[df_inpatient_2['hospital_referral_region_description'] == 'NY - East Long Island']

inpatient_sb = df_inpatient_2[df_inpatient_2['provider_city'] == 'STONY BROOK']

inpatient_li_withoutsb = inpatient_longisland[inpatient_longisland['provider_city'] != 'STONY BROOK']

st.header('Total list of DRGs and Discharges from Stony Brook Inpatients: ' )
#st.header( str(total_inpatient_count) )





##Common D/C 


#DRGs for SB
common_discharges = inpatient_sb.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.subheader('DRGs')
st.dataframe(common_discharges)

st.header('Top/Bottom 10 DRGs for Stony Brook')

col1, col2 = st.beta_columns(2)

col1.subheader('Top 10 DRGs')
col1.dataframe(top10)

col2.subheader('Bottom 10 DRGs')
col2.dataframe(bottom10)



#DRGs for other LI hospitals

st.header('Total list of DRGs and Discharges from Long Island Hospitals besides Stony Brook: ' )

common_discharges_nosb = inpatient_li_withoutsb.groupby('drg_definition')['total_discharges'].sum().reset_index()

top10_nosb = common_discharges_nosb.head(10)
bottom10_nosb = common_discharges_nosb.tail(10)

st.subheader('DRGs')
st.dataframe(common_discharges_nosb)

st.header('Top/Bottom 10 DRGs for Other LI Hospitals')

col1, col2 = st.beta_columns(2)

col1.subheader('Top 10 DRGs')
col1.dataframe(top10_nosb)

col2.subheader('Bottom 10 DRGs')
col2.dataframe(bottom10_nosb)


#DRGs SB vs LI
#st.header ('Stony Brook Total DRGs Compared to rest of LI Hospitals')
#col1, col2 = st.beta_columns(2)
#common_discharges = inpatient_sb.groupby('drg_definition')['total_discharges'].sum().reset_index()
#col1.subheader('Total DRGs for Stony Brook')
#col1.dataframe(common_discharges)
#common_discharges = inpatient_li_withoutsb.groupby('drg_definition')['total_discharges'].sum().reset_index()
#col2.subheader('Rest of LI Total DRGs')
#col2.dataframe (common_discharges)


#top DRGs SBvsLI
st.header ('Stony Brook Top DRGs Compared to Rest of LI ')

col1, col2 = st.beta_columns(2)
common_discharges = inpatient_sb.groupby('drg_definition')['total_discharges'].sum().reset_index()

top10 = common_discharges.head(10)

col1.subheader('Top 10 SB DRGs')
col1.dataframe(top10)

common_discharges_nosb = inpatient_li_withoutsb.groupby('drg_definition')['total_discharges'].sum().reset_index()

top10_nosb = common_discharges_nosb.head(10)
col2.subheader('Top 10 LI DRGs')
col2.dataframe(top10_nosb)

st.markdown ('Of the top 10 DRGs, 6 are in common between Stony Brook and the other LI hospitals.')


#Bar Charts of the costs 

#sums for all LI hospitals
costs = inpatient_longisland.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_longisland.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']

#
#costs = inpatient_longisland.groupby('provider_name')['average_total_payments'].sum().reset_index()
#costs['average_total_payments'] = costs['average_total_payments'].astype('int64')

#costs_medicare = inpatient_longisland.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
#costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')

#costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
#costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('Medicare Inpatient Payments')

st.subheader ('All Long Island Hospitals Total Inpatient Payments')
bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)
st.header("Long Island Hospitals Payments ")
st.dataframe(costs_sum)

st.markdown('Stony Brook has the highest total payments of all LI hospitals')


#DRG costs


#Costs by Condition and Hospital / Average Total Payments
#costs_condition_hospital = inpatient_li_withoutsb.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
#st.header("Costs by Condition and Hospital - Average Total Payments")
#st.dataframe(costs_condition_hospital)


costs_condition_hospital = inpatient_sb.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()

st.header("Payments by DRG for Stony Brook")
bar3 = px.bar(costs_condition_hospital, x='drg_definition', y='average_total_payments')
st.plotly_chart(bar3)
st.dataframe(costs_condition_hospital)


costs_condition_hospital = inpatient_li_withoutsb.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()

st.header("Payments by DRG for Other LI Hospitals")
bar3 = px.bar(costs_condition_hospital, x='drg_definition', y='average_total_payments')
st.plotly_chart(bar3)
st.dataframe(costs_condition_hospital)


#costs for top 10 DRG
st.header('Payments of Top 10 DRGs')
common_discharges = inpatient_sb.groupby('drg_definition')['average_total_payments'].sum().reset_index()
commontop10 = common_discharges.head(10)
st.subheader("Payments of Top 10 DRG for Stony Brook")
bar3 = px.bar(commontop10, x='drg_definition', y='average_total_payments')
st.plotly_chart(bar3)
#st.dataframe(top10)

common_discharges = inpatient_li_withoutsb.groupby('drg_definition')['average_total_payments'].sum().reset_index()
commontop10 = common_discharges.head(10)
st.subheader("Payments of Top 10 DRG for Other LI Hospitals")
bar3 = px.bar(commontop10, x='drg_definition', y='average_total_payments')
st.plotly_chart(bar3)
#st.dataframe(commontop10)

st.markdown('Stony Brook receives more payments from DRG 003 than DRG 004 _compared_ to other LI Hospitals')
st.markdown ('Stony Brook receives more payments from DRG 025 than 026 and 027, which is similar to other area hospitals. Though, they receive more payments for 026 and 027 **proportionally** compared to other LI hospitals')






st.stop()







