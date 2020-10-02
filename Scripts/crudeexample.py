import pandas as pd
import numpy as np
import datetime
from datetime import date
from xbbg import blp
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#csv file with bbg country/ticker legend
filename = 'C:\\Users\\fmocanu\\Downloads\\bbg_tickers.csv'
df_leg = pd.read_csv(filename, low_memory=False)

today = date.today()
startdate = datetime.datetime(2019,1,1)
enddate = datetime.datetime(2020,12,31)

#importing all unique ticker series
tix = df_leg['Ticker'].unique()
df = blp.bdh(tickers= tix, flds=['px_last'], start_date=startdate, end_date= enddate, Per='M', Fill='B', Days='A')
df.columns = df.columns.droplevel(1)
df['Date'] = df.index - pd.to_timedelta(df.index.day - 1, unit='d') #changes date to 1st of month to fix xaxis
df.reset_index(inplace=True)
df = df.drop(['index'], axis=1)
df_melt = pd.melt(df, id_vars= ['Date'])

#merging tickers with countries into dataframe
df_merge = df_melt.merge(df_leg, left_on= 'variable', right_on= 'Ticker')
df_merge = df_merge[['Date','Country','Grade','Ticker','value']]

#creating country totals dataframe
df_sums = df_merge.groupby(['Country','Date'])['value'].apply(pd.DataFrame.sum, skipna=False).reset_index()
df_sums = df_sums[['Date','Country','value']]
#df_sums['value']=df_sums['value'].replace(0,np.nan)

#data visualization
# Load data
df = df_sums
df.index = pd.to_datetime(df['Date'])

df1 = df_merge
df1.index = pd.to_datetime(df1['Date'])

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# Creates a list of dictionaries, which have the keys 'label' and 'value'. (used in dcc.Dropdown below)
def get_options(list_params):
    dict_list = []
    for i in list_params:
        dict_list.append({'label': i, 'value': i})

    return dict_list

# dropdown layout shortcuts
dd_wdt= {'size': 4, 'offset': 0}
dd_stl= {'font-size':'80%', 'font-weight': 400, 'color': 'black',
         'display': 'flex', 'justify-content': 'center', 'margin-top':'1%'}
head_stl = {'margin-top':'1%', 'text-align': 'center'}


#design the app
app.layout = html.Div([
        dbc.Row(dbc.Col(html.H3('Crude Loading Programs (b/d)'),
                        width={'size': 12}, style= head_stl
                        ),
                ),
        dbc.Row([
                dbc.Col(dcc.Dropdown(id='a_dropdown', placeholder='first dropdown',
                                     options=get_options(df['Country'].unique()),
                                     multi=True, value=['BRITAIN','DENMARK','NORWAY']),
                                     width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(dcc.Dropdown(id='b_dropdown', placeholder='second dropdown',
                                     options=get_options(df['Country'].unique()),
                                     multi=True, value=['ANGOLA','NIGERIA']),
                                     width= dd_wdt, style= dd_stl
                        ),
                dbc.Col(dcc.Dropdown(id='c_dropdown', placeholder='third dropdown',
                                     options=get_options(df1['Grade'].unique()),
                                     multi=True, value=['Brent','Forties','Oseberg','Ekofisk','Troll']),
                                     width= dd_wdt, style= dd_stl
                        ),
                ]),
        dbc.Row([
                dbc.Col(dcc.Graph(id='line_chart1'),
                        width=4,
                        ),
                dbc.Col(dcc.Graph(id='line_chart2'),
                        width=4,
                        ),
                dbc.Col(dcc.Graph(id='line_chart3'),
                        width=4,
                        ),
                ]),
        dbc.Row([
                dbc.Col(dcc.Dropdown(id='d_dropdown', placeholder='fourth dropdown',
                                     options=get_options(df['Country'].unique()), multi=True,
                                     value=['BRITAIN', 'DENMARK', 'NORWAY']),
                                     width= dd_wdt, style= dd_stl
                        ),
                ]),
        dbc.Row([
                dbc.Col(dcc.Graph(id='line_chart4'),
                        width=4, lg={'size': 4, "offset": 0, 'order': '1'}
                        )
                ])
])

#first chart

@app.callback(
    Output('line_chart1', 'figure'),
    [Input('a_dropdown', 'value')])

def update_graph(selected_dropdown_value):
    # Draw traces of the feature 'value' based on the currently selected country
    trace1 = []
    df_sub = df
    # Draw and append traces for each country
    for country in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['Country'] == country]['Date'],
                                 y=df_sub[df_sub['Country'] == country]['value'],
                                 mode='lines+markers',
                                 line_shape='spline',
                                 opacity=0.7,
                                 name=country,
                                 ))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist] #flattening the nested list
    # Define figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 2,'l':2,'r':2},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'North Sea (b/d)', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()], 'dtick': 'M1','tickformat':'%b%y'},
                  legend=dict(orientation='h',yanchor="bottom", y=1.02, xanchor="left", x=0)
              ),

              }

    return figure

#second chart

@app.callback(
    Output('line_chart2', 'figure'),
    [Input('b_dropdown', 'value')])

def update_graph(selected_dropdown_value):
    # Draw traces of the feature 'value' based on the currently selected country
    trace1 = []
    df_sub = df
    # Draw and append traces for each country
    for country in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['Country'] == country]['Date'],
                                 y=df_sub[df_sub['Country'] == country]['value'],
                                 mode='lines+markers',
                                 line_shape='spline',
                                 opacity=0.7,
                                 name=country,
                                 ))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    # Define figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 2,'l':2,'r':2},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'WAF (b/d)', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()], 'dtick': 'M1','tickformat':'%b%y'},
                  legend=dict(orientation='h',yanchor="bottom", y=1.02, xanchor="left", x=0)
              ),

              }

    return figure

#third chart

@app.callback(
    Output('line_chart3', 'figure'),
    [Input('c_dropdown', 'value')])

def update_graph(selected_dropdown_value):
    # Draw traces of the feature 'value' based on the currently selected country
    trace1 = []
    df_sub = df1
    # Draw and append traces for each country
    for grade in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['Grade'] == grade]['Date'],
                                 y=df_sub[df_sub['Grade'] == grade]['value'],
                                 mode='lines+markers',
                                 line_shape='spline',
                                 opacity=0.7,
                                 name=grade,
                                 ))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    # Define figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 2,'l':2,'r':2},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'BFOET (b/d)', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()], 'dtick': 'M1','tickformat':'%b%y'},
                  legend=dict(orientation='h',yanchor="bottom", y=1.02, xanchor="left", x=0)
              ),

              }

    return figure


# fourth chart

@app.callback(
    Output('line_chart4', 'figure'),
    [Input('d_dropdown', 'value')])

def update_graph(selected_dropdown_value):
    filt_df = df_sums.loc[df_sums['Country'].isin(selected_dropdown_value)]
    filt_df = filt_df.groupby(filt_df['Date'], as_index=True)['value'].sum().to_frame()
    filt_df['value'] = filt_df['value'].replace(0, np.nan)

    data = go.Scatter(x=filt_df.index,
                      y=filt_df.iloc[:,0],
                      mode='lines+markers',
                      line_shape='spline',
                      opacity=0.7,
                      name='Sum',
                      )

    layout = go.Layout(
                      colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                      template='plotly_dark',
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      margin={'b': 2,'l':2,'r':2},
                      hovermode='x',
                      autosize=True,
                      title={'text': 'Regional Sum (b/d)', 'font': {'color': 'white'}, 'x': 0.5},
                      xaxis={'range': [filt_df.index.min(), filt_df.index.max()], 'dtick': 'M1','tickformat':'%b%y'},
                      legend=dict(orientation='h',yanchor="bottom", y=1.02, xanchor="left", x=0)
                      )

    figure = go.Figure(data,layout)
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)


