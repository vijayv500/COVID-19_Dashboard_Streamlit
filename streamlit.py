import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: red;'>COVID-19 India Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
* This dashboard was created using the dataset from [Kaggle](https://www.kaggle.com/sudalairajkumar/covid19-in-india). Github Repo [here](https://github.com/vijayv500/COVID-19_Dashboard_Streamlit)
* For State-wise trends, scroll down and select a state/Union Territory from the dropdown menu.
* If the charts are displayed truncated then hover your mouse over them and use 'expand' option.
* All the below charts as per data updated till August 11, 2021 in the dataset.
* Created By [Vijay Vankayalapati](https://linktr.ee/vijayv500)
""")
st.markdown("<h2 style='text-align: center; color: green;'>All-India Trends</h2>", unsafe_allow_html=True)
df = pd.read_csv('covid_19_india.csv')

df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Bihar****':'Bihar'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Madhya Pradesh***':'Madhya Pradesh'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Maharashtra***':'Maharashtra'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Maharashtra***':'Maharashtra'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Telengana':'Telangana'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Karanataka':'Karnataka'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Dadra and Nagar Haveli':'Dadra and Nagar Haveli and Daman and Diu'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Daman & Diu':'Dadra and Nagar Haveli and Daman and Diu'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Himanchal Pradesh':'Himachal Pradesh'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Cases being reassigned to states':'Unassigned'})

state_grp = df.groupby('State/UnionTerritory').agg({'Cured': 'max','Confirmed': 'max','Deaths': 'max'})

col1, col2, col3,col4 = st.columns(4)
col1.metric("Total Confirmed Cases",int(state_grp['Confirmed'].sum()))
col2.metric("Total Cured", int(state_grp['Cured'].sum()))
col3.metric("Deaths",int(state_grp['Deaths'].sum()))
col4.metric("Active", int((state_grp['Confirmed'].sum() - state_grp['Cured'].sum()) - state_grp['Deaths'].sum()))



date_grp = df.groupby('Date').agg({'Cured': 'sum','Confirmed': 'sum','Deaths': 'sum'})
date_grp['Active'] = date_grp['Confirmed'] - date_grp['Cured']
date_grp['daily_cured'] = date_grp['Cured'].diff()
date_grp['daily_confirmed'] = date_grp['Confirmed'].diff()
date_grp['daily_deaths'] = date_grp['Deaths'].diff()

months = date_grp.index.tolist()
deaths = date_grp['Deaths'].tolist()
fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=deaths,text=deaths,line = dict(color='OrangeRed'),
                    mode='lines'))

fig.update_layout(title_text="<b>Deaths</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=0.5,
        showgrid = False)

fig.update_yaxes(
        color='Teal',
        title_text='No. of Deaths',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=1,
        showgrid = False)

months = date_grp.index.tolist()
confirmed = date_grp['Confirmed'].tolist()
cured = date_grp['Cured'].tolist()
active = date_grp['Active'].tolist()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=months, y=confirmed,text=confirmed,line = dict(color='Green'),
                    mode='lines', name = 'Confirmed'))
fig1.add_trace(go.Scatter(x=months, y=cured,text=cured,line = dict(color='Red'),
                    mode='lines', name = 'Cured'))
fig1.add_trace(go.Scatter(x=months, y=active,text=active,line = dict(color='blue'),
                    mode='lines', name = 'Active'))
fig1.update_layout(title_text="<b>Cured, Confirmed and Active Cases</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid = False)

fig1.update_yaxes(
        color='Teal',
        title_text='No. of Cases',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid = False)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig1)

#-------------------------------------------------------------------------------------------
months = date_grp.index.tolist()
daily_deaths = date_grp['daily_deaths'].tolist()
fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=daily_deaths,text=daily_deaths,line = dict(color='OrangeRed'),
                    mode='lines'))
fig.update_layout(title_text="<b>Deaths (Daily Basis)</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid = False)

fig.update_yaxes(
        color='Teal',
        title_text='No. of Deaths',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid = False)

months = date_grp.index.tolist()
daily_confirmed = date_grp['daily_confirmed'].tolist()
daily_cured = date_grp['daily_cured'].tolist()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=months, y=daily_confirmed,text=daily_confirmed,line = dict(color='Green'),
                    mode='lines', name = 'Confirmed'))
fig1.add_trace(go.Scatter(x=months, y=daily_cured,text=daily_cured,line = dict(color='Red'),
                    mode='lines', name = 'Cured'))
fig1.update_layout(title_text="<b>Cured and Confirmed Cases (Daily Basis)</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig1.update_yaxes(
        color='Teal',
        title_text='No. of Cases',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig)
with col4:
    st.plotly_chart(fig1)

#.............................................................
state_grp = df.groupby('State/UnionTerritory').agg({'Cured': 'max','Confirmed': 'max', 'Deaths': 'max'})

df_top_deaths = state_grp.sort_values(by='Deaths', ascending = False)
df_top_deaths = df_top_deaths['Deaths']

fig = px.bar(df_top_deaths[0:20],y=df_top_deaths[0:20].index, x='Deaths', text='Deaths', color='Deaths',
             color_continuous_scale = 'viridis', orientation = 'h')

fig.update_traces(textposition='outside')
fig.update_layout(title_text="<b>Top 20 States (No. of Deaths)</b>",
                 title_font_size=25,
                 title_font_color='green',
                 title_font_family='Titillium Web',
                 title_x=0.47,
                 title_y=0.95,
                 title_xanchor='center',
                 title_yanchor='top',
                 yaxis={'categoryorder':'total ascending'}
                 )

fig.update_yaxes(
        color='teal',
        title_text='State/Union Territory',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        linecolor='red',
        linewidth=3,
        mirror=True,
        showgrid=False)

fig.update_xaxes(
        color='Teal',
        title_text='No. of Deaths',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        tickfont_family='Arial',
        nticks = 20,
        gridcolor='lightblue',
        linecolor='red',
        linewidth=3,
        mirror = True,
        showgrid=False)

df_top_confirmed = state_grp.sort_values(by='Confirmed', ascending = False)
df_top_confirmed = df_top_confirmed['Confirmed']

fig1 = px.bar(df_top_confirmed[0:20],y=df_top_confirmed[0:20].index, x='Confirmed', text='Confirmed',
             color='Confirmed', color_continuous_scale = 'Hot', orientation='h')

fig1.update_traces(textposition='outside')
fig1.update_layout(title_text="<b>Top 20 States (No. of Confirmed Cases)</b>",
                 title_font_size=25,
                 title_font_color='green',
                 title_font_family='Titillium Web',
                 title_x=0.47,
                 title_y=0.95,
                 title_xanchor='center',
                 title_yanchor='top',
                 yaxis={'categoryorder':'total ascending'}
                 )

fig1.update_yaxes(
        color='teal',
        title_text='State/Union Territory',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        linecolor='red',
        linewidth=3,
        mirror=True,
        showgrid=False)

fig1.update_xaxes(
        color='Teal',
        title_text='No. of Confirmed Cases',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        tickfont_family='Arial',
        nticks = 20,
        gridcolor='lightblue',
        linecolor='red',
        linewidth=3,
        mirror = True,
        showgrid=False)

col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(fig)
with col6:
    st.plotly_chart(fig1)

#...............................................................................

df = pd.read_csv('covid_vaccine_statewise.csv')
df['Updated On'] = pd.to_datetime(df['Updated On'], format="%d/%m/%Y")
filt = (df['State']=='India')
df_india = df.loc[filt]

months = df_india['Updated On'].tolist()
doses = df_india['Total Doses Administered'].tolist()
first_doses = df_india['First Dose Administered'].tolist()
second_doses = df_india['Second Dose Administered'].tolist()
fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=doses,text=doses,line = dict(color='OrangeRed'),
                    mode='lines', name = 'Overall'))
fig.add_trace(go.Scatter(x=months, y=first_doses,text=first_doses,line = dict(color='blue'),
                    mode='lines', name = '1st Dose'))
fig.add_trace(go.Scatter(x=months, y=second_doses,text=second_doses,line = dict(color='green'),
                    mode='lines', name = '2nd Dose'))
fig.update_layout(title_text="<b>Total Vaccine Doses Administered</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig.update_yaxes(
        color='Teal',
        title_text='No. of Doses',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

months = df_india['Updated On'].tolist()

age_1 = df_india['18-44 Years(Individuals Vaccinated)'].tolist()
age_2 = df_india['45-60 Years(Individuals Vaccinated)'].tolist()
age_3 = df_india['60+ Years(Individuals Vaccinated)'].tolist()
age_4 = df_india['Total Individuals Vaccinated'].tolist()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=months, y=age_1,text=age_1,line = dict(color='OrangeRed'),
                    mode='lines', name = '18-44 Years'))
fig1.add_trace(go.Scatter(x=months, y=age_2,text=age_2,line = dict(color='blue'),
                    mode='lines', name = '45-60 Years'))
fig1.add_trace(go.Scatter(x=months, y=age_3,text=age_3,line = dict(color='green'),
                    mode='lines', name = '60+ Years'))
fig1.add_trace(go.Scatter(x=months, y=age_4,text=age_4,line = dict(color='brown'),
                    mode='lines', name = 'Overall'))
fig1.update_layout(title_text="<b>Age Groups - Vaccinated Individuals</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig1.update_yaxes(
        color='Teal',
        title_text='No. of Doses',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

col7, col8 = st.columns(2)

with col7:
    st.plotly_chart(fig)
with col8:
    st.plotly_chart(fig1)

#.......................................................
state_grp = df.groupby('State').agg({'Total Individuals Vaccinated':'max',
                                    'Total Doses Administered':'max'})
df_states = state_grp.sort_values(by='Total Doses Administered', ascending = False)
fig = px.bar(df_states[1:21],y=df_states[1:21].index, x='Total Doses Administered',
             text='Total Doses Administered', color='Total Doses Administered',
             color_continuous_scale = 'viridis', orientation='h')

fig.update_traces(textposition='outside')
fig.update_layout(title_text="<b>Top 20 States (Total Vaccine Doses Administered)</b>",
                 title_font_size=25,
                 title_font_color='green',
                 title_font_family='Titillium Web',
                 title_x=0.47,
                 title_y=0.95,
                 title_xanchor='center',
                 title_yanchor='top',
                 yaxis={'categoryorder':'total ascending'}
                 )

fig.update_yaxes(
        color='teal',
        title_text='State/Union Territory',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        linecolor='red',
        linewidth=3,
        mirror=True,
        showgrid=False)

fig.update_xaxes(
        color='Teal',
        title_text='No. of Deaths',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        tickfont_family='Arial',
        nticks = 20,
        gridcolor='lightblue',
        linecolor='red',
        linewidth=3,
        mirror = True,
        showgrid=False)
df_states = state_grp.sort_values(by='Total Individuals Vaccinated', ascending = False)
fig1 = px.bar(df_states[1:21],y=df_states[1:21].index, x='Total Individuals Vaccinated',
             text='Total Individuals Vaccinated', color='Total Individuals Vaccinated',
             color_continuous_scale = 'viridis', orientation='h')

fig1.update_traces(textposition='outside')
fig1.update_layout(title_text="<b>Top 20 States (No. of Individuals Fully Vaccinated)</b>",
                 title_font_size=25,
                 title_font_color='green',
                 title_font_family='Titillium Web',
                 title_x=0.47,
                 title_y=0.95,
                 title_xanchor='center',
                 title_yanchor='top',
                 yaxis={'categoryorder':'total ascending'}
                 )

fig1.update_yaxes(
        color='teal',
        title_text='State/Union Territory',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        linecolor='red',
        linewidth=3,
        mirror=True,
        showgrid=False)

fig1.update_xaxes(
        color='Teal',
        title_text='No. of Deaths',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='maroon',
        title_standoff = 15,
        tickfont_family='Arial',
        nticks = 20,
        gridcolor='lightblue',
        linecolor='red',
        linewidth=3,
        mirror = True,
        showgrid=False)

col9, col10 = st.columns(2)
with col9:
    st.plotly_chart(fig)
with col10:
    st.plotly_chart(fig1)

#...............................................................

df_daily = pd.read_csv("daily_cases.csv")
df_daily['Date'] = pd.to_datetime(df_daily['Date'], format = "%Y-%m-%d")
df_india = df_india.rename(columns = {'Updated On':'Date'})
df_new = pd.merge(df_daily,df_india, on = 'Date' )
df_new['daily_doses'] = df_new['Total Doses Administered'].diff()

months = df_new['Date'].tolist()
age_1 = df_new['Total Doses Administered'].tolist()
age_2 = df_new['Deaths'].tolist()
fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=age_1,text=age_1,line = dict(color='OrangeRed'),
                    mode='lines', name = 'Doses'))
fig.add_trace(go.Scatter(x=months, y=age_2,text=age_2,line = dict(color='blue'),
                    mode='lines', name = 'Deaths'))
fig.update_layout(title_text="<b>Vaccine Doses vs Deaths (log scale)</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig.update_yaxes(
        type="log",
        color='Teal',
        title_text='Count (log scale)',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

months = df_india['Date'].tolist()
covaxin = df_india[' Covaxin (Doses Administered)'].tolist()
covishield = df_india['CoviShield (Doses Administered)'].tolist()
sputnik = df_india['Sputnik V (Doses Administered)'].tolist()


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=months, y=covaxin,text=covaxin,line = dict(color='OrangeRed'),
                    mode='lines', name = 'Covaxin'))
fig1.add_trace(go.Scatter(x=months, y=covishield,text=covishield,line = dict(color='blue'),
                    mode='lines', name = 'Covishield'))
fig1.add_trace(go.Scatter(x=months, y=sputnik,text=sputnik,line = dict(color='green'),
                    mode='lines', name = 'Sputnik'))

fig1.update_layout(title_text="<b>Types of Vaccines Administered(log scale)</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig1.update_yaxes(
        type='log',
        color='Teal',
        title_text='No. of Doses (log scale)',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

col11, col12 = st.columns(2)
with col11:
    st.plotly_chart(fig)
with col12:
    st.plotly_chart(fig1)

#......................................................

st.subheader("Select an Option From Below For State-wise Trends")

#............................................states.......#

df = pd.read_csv('covid_19_india.csv')
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Bihar****':'Bihar'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Madhya Pradesh***':'Madhya Pradesh'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Maharashtra***':'Maharashtra'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Maharashtra***':'Maharashtra'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Telengana':'Telangana'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Karanataka':'Karnataka'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Dadra and Nagar Haveli':'Dadra and Nagar Haveli and Daman and Diu'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Daman & Diu':'Dadra and Nagar Haveli and Daman and Diu'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Himanchal Pradesh':'Himachal Pradesh'})
df['State/UnionTerritory'] = df['State/UnionTerritory'].replace({'Cases being reassigned to states':'Unassigned'})

state_list = list(df['State/UnionTerritory'].unique())
state_list.remove('Unassigned')
state_chosen = st.selectbox('Select State/UT',state_list)
st.markdown(f"<h2 style='text-align: center; color: green;'>Trends For {state_chosen}</h2>", unsafe_allow_html=True)
filt = (df['State/UnionTerritory'] == state_chosen)
df = df.loc[filt]
df['Active'] = df['Confirmed'] - df['Cured']

col1, col2, col3,col4 = st.columns(4)
col1.metric("Total Confirmed Cases",int(df['Confirmed'].max()))
col2.metric("Total Cured", int(df['Cured'].max()))
col3.metric("Deaths",int(df['Deaths'].max()))
col4.metric("Active", int((df['Confirmed'].max() - df['Cured'].max()) - df['Deaths'].max()))



months = df['Date'].tolist()
deaths = df['Deaths'].tolist()

fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=deaths,text=deaths,line = dict(color='OrangeRed'),
                    mode='lines'))
fig.update_layout(title_text=f"<b>Deaths ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig.update_yaxes(
        color='Teal',
        title_text='No. of Deaths',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)


months = df['Date'].tolist()
confirmed = df['Confirmed'].tolist()
cured = df['Cured'].tolist()
active = df['Active'].tolist()

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=months, y=confirmed,text=confirmed,line = dict(color='Green'),
                    mode='lines', name = 'Confirmed'))
fig1.add_trace(go.Scatter(x=months, y=cured,text=cured,line = dict(color='Red'),
                    mode='lines', name = 'Cured'))
fig1.add_trace(go.Scatter(x=months, y=active,text=active,line = dict(color='blue'),
                    mode='lines', name = 'Active'))


fig1.update_layout(title_text=f"<b>Cured, Confirmed and Active Cases ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid = False)

fig1.update_yaxes(
        color='Teal',
        title_text='No. of Cases',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid = False)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig1)

#.......................................
df['daily_cured'] = df['Cured'].diff()
df['daily_confirmed'] = df['Confirmed'].diff()
df['daily_deaths'] = df['Deaths'].diff()

months = df['Date'].tolist()
daily_deaths = df['daily_deaths'].tolist()
fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=daily_deaths,text=daily_deaths,line = dict(color='OrangeRed'),
                    mode='lines'))
fig.update_layout(title_text=f"<b>Deaths (Daily Basis) ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid = False)

fig.update_yaxes(
        color='Teal',
        title_text='No. of Deaths',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid = False)

months = df['Date'].tolist()
daily_confirmed = df['daily_confirmed'].tolist()
daily_cured = df['daily_cured'].tolist()


fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=months, y=daily_confirmed,text=daily_confirmed,line = dict(color='Green'),
                    mode='lines', name = 'Confirmed'))
fig1.add_trace(go.Scatter(x=months, y=daily_cured,text=daily_cured,line = dict(color='Red'),
                    mode='lines', name = 'Cured'))



fig1.update_layout(title_text=f"<b>Cured and Confirmed Cases (Daily Basis) ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig1.update_yaxes(
        color='Teal',
        title_text='No. of Cases',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig1)

#...............................................
df = pd.read_csv('covid_vaccine_statewise.csv')
df['Updated On'] = pd.to_datetime(df['Updated On'], format="%d/%m/%Y")
filt = (df['State']==state_chosen)
df = df.loc[filt]

months = df['Updated On'].tolist()
doses = df['Total Doses Administered'].tolist()

first_doses = df['First Dose Administered'].tolist()
second_doses = df['Second Dose Administered'].tolist()


fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=doses,text=doses,line = dict(color='OrangeRed'),
                    mode='lines', name = 'Total Doses'))
fig.add_trace(go.Scatter(x=months, y=first_doses,text=first_doses,line = dict(color='blue'),
                    mode='lines', name = 'First Dose'))
fig.add_trace(go.Scatter(x=months, y=second_doses,text=second_doses,line = dict(color='green'),
                    mode='lines', name = 'Second Dose'))


fig.update_layout(title_text=f"<b>Total Vaccine Doses Administered ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig.update_yaxes(
        color='Teal',
        title_text='No. of Doses',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

months = df['Updated On'].tolist()

age_1 = df['18-44 Years(Individuals Vaccinated)'].tolist()
age_2 = df['45-60 Years(Individuals Vaccinated)'].tolist()
age_3 = df['60+ Years(Individuals Vaccinated)'].tolist()
age_4 = df['Total Individuals Vaccinated'].tolist()

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=months, y=age_1,text=age_1,line = dict(color='OrangeRed'),
                    mode='lines', name = '18-44 Years'))
fig1.add_trace(go.Scatter(x=months, y=age_2,text=age_2,line = dict(color='blue'),
                    mode='lines', name = '45-60 Years'))
fig1.add_trace(go.Scatter(x=months, y=age_3,text=age_3,line = dict(color='green'),
                    mode='lines', name = '60+ Years'))
fig1.add_trace(go.Scatter(x=months, y=age_4,text=age_4,line = dict(color='brown'),
                    mode='lines', name = 'Overall'))


fig1.update_layout(title_text=f"<b>Age Groups - Vaccinated Individuals ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig1.update_yaxes(
        color='Teal',
        title_text='No. of Doses',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig1)

#......................................

df_daily = pd.read_csv("daily_cases.csv")
df_daily['Date'] = pd.to_datetime(df_daily['Date'], format = "%Y-%m-%d")
df = df.rename(columns = {'Updated On':'Date'})
df_new = pd.merge(df_daily,df, on = 'Date' )
months = df_new['Date'].tolist()

age_1 = df_new['Total Doses Administered'].tolist()
age_2 = df_new['Deaths'].tolist()

fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=age_1,text=age_1,line = dict(color='OrangeRed'),
                    mode='lines', name = 'Doses'))
fig.add_trace(go.Scatter(x=months, y=age_2,text=age_2,line = dict(color='blue'),
                    mode='lines', name = 'Deaths'))


fig.update_layout(title_text=f"<b>Vaccine Doses vs Deaths (log scale) ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3,
        showgrid=False)

fig.update_yaxes(
        type="log",
        color='Teal',
        title_text='Count (log scale)',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3,
        showgrid=False)

months = df['Date'].tolist()
covaxin = df[' Covaxin (Doses Administered)'].tolist()
covishield = df['CoviShield (Doses Administered)'].tolist()
sputnik = df['Sputnik V (Doses Administered)'].tolist()


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=months, y=covaxin,text=covaxin,line = dict(color='OrangeRed'),
                    mode='lines', name = 'Covaxin'))
fig1.add_trace(go.Scatter(x=months, y=covishield,text=covishield,line = dict(color='blue'),
                    mode='lines', name = 'Covishield'))
fig1.add_trace(go.Scatter(x=months, y=sputnik,text=sputnik,line = dict(color='green'),
                    mode='lines', name = 'Sputnik'))


fig1.update_layout(title_text=f"<b>Types of Vaccines (log scale) ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig1.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3)

fig1.update_yaxes(
        type='log',
        color='Teal',
        title_text='No. of Doses (log scale)',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig1)

#.....................................................
df = pd.read_csv('StatewiseTestingDetails.csv')
filt = (df['State']==state_chosen)
df = df.loc[filt]
df['daily_tests'] = df['TotalSamples'].diff()

months = df['Date'].tolist()
samples = df['TotalSamples'].tolist()

fig = go.Figure()
fig.add_trace(go.Scatter(x=months, y=samples,text=samples,line = dict(color='OrangeRed'),
                    mode='lines'))

fig.update_layout(title_text=f"<b>COVID-19 Tests ({state_chosen})</b>",
                 title_font_size=25,
                 title_font_color='RoyalBlue',
                 title_font_family='Titillium Web',
                 title_x=0.5,
                 title_y=0.87,
                 title_xanchor='center',
                 title_yanchor='top')

fig.update_xaxes(
        color='ForestGreen',
        title_font_family='Open Sans',
        title_font_size=20,
        title_font_color='Crimson',
        title_standoff = 15,
        gridcolor='lightblue',
        tickmode='auto',
        nticks=18,
        linecolor='black',
        linewidth=3)

fig.update_yaxes(
        color='Teal',
        title_text='No. of Tests',
        title_font_family='Droid Sans',
        title_font_size=20,
        title_font_color='Teal',
        title_standoff = 15,
        tickfont_family='Arial',
        gridcolor='lightblue',
        linecolor='black',
        linewidth=3)

months = df['Date'].tolist()
samples = df['daily_tests'].tolist()

fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=months, y=samples, text=samples, line=dict(color='OrangeRed'),
                         mode='lines'))

fig1.update_layout(title_text=f"<b>Daily Testing ({state_chosen})</b>",
                  title_font_size=25,
                  title_font_color='RoyalBlue',
                  title_font_family='Titillium Web',
                  title_x=0.5,
                  title_y=0.87,
                  title_xanchor='center',
                  title_yanchor='top')

fig1.update_xaxes(
    color='ForestGreen',
    title_font_family='Open Sans',
    title_font_size=20,
    title_font_color='Crimson',
    title_standoff=15,
    gridcolor='lightblue',
    tickmode='auto',
    nticks=18,
    linecolor='black',
    linewidth=3)

fig1.update_yaxes(
    color='Teal',
    title_text='No. of Tests',
    title_font_family='Droid Sans',
    title_font_size=20,
    title_font_color='Teal',
    title_standoff=15,
    tickfont_family='Arial',
    gridcolor='lightblue',
    linecolor='black',
    linewidth=3)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig1)


























