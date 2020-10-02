import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# importing data from database
# DB Details
connection_type = "mssql+pyodbc"
dataportal_db_user = "dataportal"
dataportal_db_password = "FatShamingMarc"
dataportal_db_ip = "10.8.4.35"
db_port = "1433"
db_prod_name = "dataportal_prod"
db_driver = "ODBC+DRIVER+17+for+SQL+Server"

def create_connection_string(connection_type, user, password, host, port, database_name, driver):
    return (
        "{connection_type}://{user}:{password}@{host}:{port}/{database_name}"
        "?driver={driver}").format(
        connection_type=connection_type,
        user=user,
        password=password,
        host=host,
        port=port,
        database_name=database_name,
        driver=driver)

connection_string = create_connection_string(connection_type,dataportal_db_user,dataportal_db_password,dataportal_db_ip,db_port,db_prod_name, db_driver)
engine = create_engine(connection_string, poolclass=StaticPool)


grouped_df = df.groupby(['EVENT_START', 'EVENT_END', 'COUNTRY',
                         'EVENT_TYPE', 'UNIT_TYPE_DESCRIPTION']).agg({"CAPACITY_OFFLINE": "sum"}).reset_index()

# adding region column to grouped_df based on below dictionary
country_mappings= {
    'GLOBAL': 'GLOBAL',
    'CANADA': 'NAM',
    'MEXICO': 'NAM',
    'U.S.A.': 'NAM',
    'AUSTRIA': 'Europe',
    'BELARUS': 'Europe',
    'BELGIUM' : 'Europe',
    'BOSNIA-HERZEGOVINA' : 'Europe',
    'CROATIA' : 'Europe',
    'CZECH REPUBLIC' : 'Europe',
    'DENMARK' : 'Europe',
    'FINLAND' : 'Europe',
    'FRANCE' : 'Europe',
    'GERMANY' : 'Europe',
    'GREECE' : 'Europe',
    'HUNGARY' : 'Europe',
    'IRELAND' : 'Europe',
    'ITALY' : 'Europe',
    'LITHUANIA' : 'Europe',
    'MACEDONIA' : 'Europe',
    'NETHERLANDS' : 'Europe',
    'NORWAY' : 'Europe',
    'POLAND' : 'Europe',
    'PORTUGAL' : 'Europe',
    'ROMANIA' : 'Europe',
    'SERBIA' : 'Europe',
    'SLOVAKIA' : 'Europe',
    'SPAIN' : 'Europe',
    'SWEDEN' : 'Europe',
    'SWITZERLAND' : 'Europe',
    'UKRAINE' : 'Europe',
    'UNITED KINGDOM' : 'Europe',
    'RUSSIA' : 'Russia',
    'CHINA' : 'China',
    'BAHRAIN' : 'Middle East',
    'JORDAN' : 'Middle East',
    'KUWAIT' : 'Middle East',
    'IRAN' : 'Middle East',
    'IRAQ' : 'Middle East',
    'ISRAEL' : 'Middle East',
    'OMAN' : 'Middle East',
    'QATAR' : 'Middle East',
    'SAUDI ARABIA' : 'Middle East',
    'SYRIA' : 'Middle East',
    'UNITED ARAB EMIRATES' : 'Middle East',
    'YEMEN' : 'Middle East'
}

cm = pd.DataFrame(list(country_mappings.items()),columns = ['COUNTRY','REGION'])
grouped_df = grouped_df.merge(cm, how = 'left', left_on='COUNTRY',right_on= 'COUNTRY')

# creating global values
grouped_df_glob = grouped_df.copy()
grouped_df_glob[['COUNTRY','REGION']] = 'GLOBAL'
grouped_df = pd.concat([grouped_df,grouped_df_glob])

# creating planned + unplanned values
grouped_df_pu = grouped_df.copy()
grouped_df_pu['EVENT_TYPE'] = 'All'
grouped_df = pd.concat([grouped_df,grouped_df_pu])

# creating multiindex df with each event as single timeseries
ix = pd.date_range(start='1970-01-01', end='2021-12-31', freq='D')

start_df = pd.pivot_table(grouped_df, index='EVENT_START', values='CAPACITY_OFFLINE',
                          columns=['REGION','EVENT_TYPE','UNIT_TYPE_DESCRIPTION'],
                          aggfunc='sum').reindex(ix).fillna(0)

end_df = pd.pivot_table(grouped_df, index='EVENT_END', values='CAPACITY_OFFLINE',
                        columns=['REGION','EVENT_TYPE','UNIT_TYPE_DESCRIPTION'],
                        aggfunc='sum').reindex(ix).fillna(0) * -1

comb_df = start_df.add(end_df).cumsum()

# 'monthalizing' dataframe
comb_df_m = comb_df.resample('M').mean()
comb_df_m['MONTH'] = comb_df_m.index.month
comb_df_m['YEAR'] = comb_df_m.index.year
comb_df_m = comb_df_m.set_index(['YEAR','MONTH'])

# dashboard creation

# initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.config.suppress_callback_exceptions = True

# Creates a list of dictionaries, which have the keys 'label' and 'value'. (used in dcc.Dropdown below)
def get_options(list_params):
    dict_list = []
    for i in list_params:
        dict_list.append({'label': i, 'value': i})

    return dict_list

# dropdown option shortcuts
country_list = df['COUNTRY'].unique().tolist()
region_list = cm['REGION'].unique().tolist()
distillation_list = grouped_df['UNIT_TYPE_DESCRIPTION'].unique().tolist()
etype_list = grouped_df['EVENT_TYPE'].unique().tolist()

# dropdown layout shortcuts
dd_wdt= {'size': 2, 'offset': 0}
dd_stl= {'font-size':'75%'}

# design the app
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Tab 1',children=[
            dbc.Row(
                dbc.Col(html.H2('Global Maintenance (b/d)'),
                        width={'size': 12, 'offset': 4}, style={'margin-top':'1%'})
                    ),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='dd_r_1', placeholder='Region',
                                 options= get_options(region_list), multi=True, value=['GLOBAL']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_r_2', placeholder='Region',
                                 options= get_options(region_list), multi=True, value=['GLOBAL']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_r_3', placeholder='Region',
                                 options= get_options(region_list),multi=True, value=['GLOBAL']),
                                 width= dd_wdt, style= dd_stl
                        )
                    ], justify='around'),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='dd_e_1', placeholder='Planned or Unplanned',
                                 options= get_options(etype_list), multi=True, value=['All']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_e_2', placeholder='Planned or Unplanned',
                                 options=get_options(etype_list), multi=True, value=['Planned']),
                                 width=dd_wdt, style=dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_e_3', placeholder='Planned or Unplanned',
                                 options=get_options(etype_list), multi=True, value=['Unplanned']),
                                 width=dd_wdt, style=dd_stl
                        )
                    ], justify='around'),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='dd_u_1', placeholder='Unit Type',
                                 options=get_options(distillation_list),
                                 multi=True, value=['Atmospheric Distillation']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_u_2', placeholder='Unit Type',
                                 options=get_options(distillation_list),
                                 multi=True, value=['Atmospheric Distillation']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_u_3', placeholder='Unit Type',
                                 options=get_options(distillation_list),
                                 multi=True, value=['Atmospheric Distillation']),
                                 width= dd_wdt, style= dd_stl
                        )
                     ], justify='around'),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='g1'),
                        width=4
                        ),
                dbc.Col(
                    dcc.Graph(id='g2'),
                        width=4
                        ),
                dbc.Col(
                    dcc.Graph(id='g3'),
                        width=4
                        ),
                    ]),
            dbc.Row(
                dbc.Col(html.H2('NAM Maintenance (b/d)'),
                        width={'size': 12, 'offset': 4}, style={'margin-top':'1%'})
                    ),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='dd_r_4', placeholder='Region',
                                 options= get_options(region_list), multi=True, value=['NAM']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_r_5', placeholder='Region',
                                 options= get_options(region_list), multi=True, value=['NAM']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_r_6', placeholder='Region',
                                 options= get_options(region_list),multi=True, value=['NAM']),
                                 width= dd_wdt, style= dd_stl
                        )
                    ], justify='around'),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='dd_e_4', placeholder='Planned or Unplanned',
                                 options= get_options(etype_list), multi=True, value=['All']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_e_5', placeholder='Planned or Unplanned',
                                 options=get_options(etype_list), multi=True, value=['Planned']),
                                 width=dd_wdt, style=dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_e_6', placeholder='Planned or Unplanned',
                                 options=get_options(etype_list), multi=True, value=['Unplanned']),
                                 width=dd_wdt, style=dd_stl
                        )
                    ], justify='around'),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='dd_u_4', placeholder='Unit Type',
                                 options=get_options(distillation_list),
                                 multi=True, value=['Atmospheric Distillation']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_u_5', placeholder='Unit Type',
                                 options=get_options(distillation_list),
                                 multi=True, value=['Atmospheric Distillation']),
                                 width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(
                    dcc.Dropdown(id='dd_u_6', placeholder='Unit Type',
                                 options=get_options(distillation_list),
                                 multi=True, value=['Atmospheric Distillation']),
                                 width= dd_wdt, style= dd_stl
                        )
                     ], justify='around'),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='g4'),
                        width=4
                        ),
                dbc.Col(
                    dcc.Graph(id='g5'),
                        width=4
                        ),
                dbc.Col(
                    dcc.Graph(id='g6'),
                        width=4
                        ),
                    ])
        ])

    ], colors={'border': 'white', 'primary': 'black', 'background': 'lightgrey'}) # tab formatting
])


# declare variables for traces
years = [2016,2017,2018,2019,2020,2021]
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
layout = go.Layout(
                  colorway=['#17becf','#e377c2','#ff7f0e','#2ca02c','black','grey'],
                  title = {'text': ' '},
                  margin={'t': 40, 'b': 40, 'l': 40, 'r': 10},
                  legend=dict(orientation='h', yanchor="bottom", y=-0.25, xanchor="left", x=0)
                   )

# function for creating graphs to apply to each callback
def update_figure(selected_dropdown_region, selected_planning_type, selected_distillation_type):

    trace = []
    # draw and append traces for each country

    for region, planning_type, distillation_type in zip(selected_dropdown_region,selected_planning_type, selected_distillation_type):
        for year in years:
            trace.append(go.Scatter(x= months,
                                     y= comb_df_m.loc[year,(region,planning_type,distillation_type)],
                                     mode = 'lines + markers',
                                     line_shape='spline',
                                     name = year))

    traces = [trace]
    data = [val for sublist in traces for val in sublist]

    # define figure for graph output

    figure = {'data': data, 'layout': layout}

    return figure

# 1st chart
@app.callback(
    Output(component_id='g1', component_property='figure'),
    [Input(component_id='dd_r_1', component_property='value'),
     Input(component_id='dd_e_1', component_property='value'),
     Input(component_id='dd_u_1', component_property='value')]
)

def update_fig1(*args):
    return update_figure(*args)

# 2nd chart
@app.callback(
    Output(component_id='g2', component_property='figure'),
    [Input(component_id='dd_r_2', component_property='value'),
     Input(component_id='dd_e_2', component_property='value'),
     Input(component_id='dd_u_2', component_property='value')]
)

def update_fig2(*args):
    return update_figure(*args)

# 3rd chart
@app.callback(
    Output(component_id='g3', component_property='figure'),
    [Input(component_id='dd_r_3', component_property='value'),
     Input(component_id='dd_e_3', component_property='value'),
     Input(component_id='dd_u_3', component_property='value')]
)

def update_fig3(*args):
    return update_figure(*args)

# 4th chart
@app.callback(
    Output(component_id='g4', component_property='figure'),
    [Input(component_id='dd_r_4', component_property='value'),
     Input(component_id='dd_e_4', component_property='value'),
     Input(component_id='dd_u_4', component_property='value')]
)

def update_fig4(*args):
    return update_figure(*args)

# 5th chart
@app.callback(
    Output(component_id='g5', component_property='figure'),
    [Input(component_id='dd_r_5', component_property='value'),
     Input(component_id='dd_e_5', component_property='value'),
     Input(component_id='dd_u_5', component_property='value')]
)

def update_fig5(*args):
    return update_figure(*args)

# 6th chart
@app.callback(
    Output(component_id='g6', component_property='figure'),
    [Input(component_id='dd_r_6', component_property='value'),
     Input(component_id='dd_e_6', component_property='value'),
     Input(component_id='dd_u_6', component_property='value')]
)

def update_fig6(*args):
    return update_figure(*args)


if __name__ == '__main__':
    app.run_server(debug=True)







