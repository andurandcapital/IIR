import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from output_actions import get_dropdown_options
from output_actions import update_figure


# dropdown layout shortcuts
dd_wdt= {'size': 2, 'offset': 0}
dd_stl= {'font-size':'75%'}

def design_dash(app, dfs_multipublish_dict, region_list, etype_list, distillation_list):
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
                                     options= get_dropdown_options(region_list), multi=True, value=['GLOBAL']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_2', placeholder='Region',
                                     options= get_dropdown_options(region_list), multi=True, value=['GLOBAL']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_3', placeholder='Region',
                                     options= get_dropdown_options(region_list), multi=True, value=['GLOBAL']),
                                     width= dd_wdt, style= dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_1', placeholder='Planned or Unplanned',
                                     options= get_dropdown_options(etype_list), multi=True, value=['All']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_2', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Planned']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_3', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Unplanned']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_1', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_2', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_3', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
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
                                     options= get_dropdown_options(region_list), multi=True, value=['NAM']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_5', placeholder='Region',
                                     options= get_dropdown_options(region_list), multi=True, value=['NAM']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_6', placeholder='Region',
                                     options= get_dropdown_options(region_list), multi=True, value=['NAM']),
                                     width= dd_wdt, style= dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_4', placeholder='Planned or Unplanned',
                                     options= get_dropdown_options(etype_list), multi=True, value=['All']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_5', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Planned']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_6', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Unplanned']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_4', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_5', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width= dd_wdt, style= dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_6', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
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
            ]),
            # second tab starts here
            dcc.Tab(label='Tab 2', children=[
                dbc.Row(
                    dbc.Col(html.H2('European Maintenance (b/d)'),
                            width={'size': 12, 'offset': 4}, style={'margin-top': '1%'})
                        ),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_7', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Europe']),
                        width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_8', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Europe']),
                        width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_9', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Europe']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_7', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['All']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_8', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Planned']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_9', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Unplanned']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_7', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_8', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_9', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='g7'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g8'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g9'),
                        width=4
                            ),
                        ]),
                dbc.Row(
                    dbc.Col(html.H2('Chinese Maintenance (b/d)'),
                            width={'size': 12, 'offset': 4}, style={'margin-top': '1%'})
                        ),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_10', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['China']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_11', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['China']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_12', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['China']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_10', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['All']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_11', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Planned']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_12', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Unplanned']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_10', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_11', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_12', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='g10'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g11'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g12'),
                        width=4
                            ),
                ])
            ]),
            # third tab starts here
            dcc.Tab(label='Tab 3', children=[
                dbc.Row(
                    dbc.Col(html.H2('Middle East Maintenance (b/d)'),
                            width={'size': 12, 'offset': 4}, style={'margin-top': '1%'})
                        ),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_13', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Middle East']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_14', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Middle East']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_15', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Middle East']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_13', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['All']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_14', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Planned']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_15', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Unplanned']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_13', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_14', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_15', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='g13'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g14'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g15'),
                        width=4
                            ),
                        ]),
                dbc.Row(
                    dbc.Col(html.H2('Russia Maintenance (b/d)'),
                            width={'size': 12, 'offset': 4}, style={'margin-top': '1%'})
                        ),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_16', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Russia']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_17', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Russia']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_r_18', placeholder='Region',
                                     options=get_dropdown_options(region_list), multi=True, value=['Russia']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_16', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['All']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_17', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Planned']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_e_18', placeholder='Planned or Unplanned',
                                     options=get_dropdown_options(etype_list), multi=True, value=['Unplanned']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_16', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_17', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            ),
                    dbc.Col(
                        dcc.Dropdown(id='dd_u_18', placeholder='Unit Type',
                                     options=get_dropdown_options(distillation_list),
                                     multi=True, value=['Atmospheric Distillation']),
                                     width=dd_wdt, style=dd_stl
                            )
                        ], justify='around'),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='g16'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g17'),
                        width=4
                            ),
                    dbc.Col(
                        dcc.Graph(id='g18'),
                        width=4
                            ),
                ])
            ])
        ], colors={'border': 'white', 'primary': 'black', 'background': 'lightgrey'}) # tab formatting
    ])

    # 1st chart
    @app.callback(
        Output(component_id='g1', component_property='figure'),
        [Input(component_id='dd_r_1', component_property='value'),
         Input(component_id='dd_e_1', component_property='value'),
         Input(component_id='dd_u_1', component_property='value')]
    )
    def update_fig1(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 2nd chart
    @app.callback(
        Output(component_id='g2', component_property='figure'),
        [Input(component_id='dd_r_2', component_property='value'),
         Input(component_id='dd_e_2', component_property='value'),
         Input(component_id='dd_u_2', component_property='value')]
    )
    def update_fig2(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 3rd chart
    @app.callback(
        Output(component_id='g3', component_property='figure'),
        [Input(component_id='dd_r_3', component_property='value'),
         Input(component_id='dd_e_3', component_property='value'),
         Input(component_id='dd_u_3', component_property='value')]
    )
    def update_fig3(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 4th chart
    @app.callback(
        Output(component_id='g4', component_property='figure'),
        [Input(component_id='dd_r_4', component_property='value'),
         Input(component_id='dd_e_4', component_property='value'),
         Input(component_id='dd_u_4', component_property='value')]
    )
    def update_fig4(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 5th chart
    @app.callback(
        Output(component_id='g5', component_property='figure'),
        [Input(component_id='dd_r_5', component_property='value'),
         Input(component_id='dd_e_5', component_property='value'),
         Input(component_id='dd_u_5', component_property='value')]
    )
    def update_fig5(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 6th chart
    @app.callback(
        Output(component_id='g6', component_property='figure'),
        [Input(component_id='dd_r_6', component_property='value'),
         Input(component_id='dd_e_6', component_property='value'),
         Input(component_id='dd_u_6', component_property='value')]
    )
    def update_fig6(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 7th chart
    @app.callback(
        Output(component_id='g7', component_property='figure'),
        [Input(component_id='dd_r_7', component_property='value'),
         Input(component_id='dd_e_7', component_property='value'),
         Input(component_id='dd_u_7', component_property='value')]
    )
    def update_fig7(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 8th chart
    @app.callback(
        Output(component_id='g8', component_property='figure'),
        [Input(component_id='dd_r_8', component_property='value'),
         Input(component_id='dd_e_8', component_property='value'),
         Input(component_id='dd_u_8', component_property='value')]
    )
    def update_fig8(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 9th chart
    @app.callback(
        Output(component_id='g9', component_property='figure'),
        [Input(component_id='dd_r_9', component_property='value'),
         Input(component_id='dd_e_9', component_property='value'),
         Input(component_id='dd_u_9', component_property='value')]
    )
    def update_fig9(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 10th chart
    @app.callback(
        Output(component_id='g10', component_property='figure'),
        [Input(component_id='dd_r_10', component_property='value'),
         Input(component_id='dd_e_10', component_property='value'),
         Input(component_id='dd_u_10', component_property='value')]
    )
    def update_fig10(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 11th chart
    @app.callback(
        Output(component_id='g11', component_property='figure'),
        [Input(component_id='dd_r_11', component_property='value'),
         Input(component_id='dd_e_11', component_property='value'),
         Input(component_id='dd_u_11', component_property='value')]
    )
    def update_fig11(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 12th chart
    @app.callback(
        Output(component_id='g12', component_property='figure'),
        [Input(component_id='dd_r_12', component_property='value'),
         Input(component_id='dd_e_12', component_property='value'),
         Input(component_id='dd_u_12', component_property='value')]
    )
    def update_fig12(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 13th chart
    @app.callback(
        Output(component_id='g13', component_property='figure'),
        [Input(component_id='dd_r_13', component_property='value'),
         Input(component_id='dd_e_13', component_property='value'),
         Input(component_id='dd_u_13', component_property='value')]
    )
    def update_fig13(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 14th chart
    @app.callback(
        Output(component_id='g14', component_property='figure'),
        [Input(component_id='dd_r_14', component_property='value'),
         Input(component_id='dd_e_14', component_property='value'),
         Input(component_id='dd_u_14', component_property='value')]
    )
    def update_fig14(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 15th chart
    @app.callback(
        Output(component_id='g15', component_property='figure'),
        [Input(component_id='dd_r_15', component_property='value'),
         Input(component_id='dd_e_15', component_property='value'),
         Input(component_id='dd_u_15', component_property='value')]
    )
    def update_fig15(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 16th chart
    @app.callback(
        Output(component_id='g16', component_property='figure'),
        [Input(component_id='dd_r_16', component_property='value'),
         Input(component_id='dd_e_16', component_property='value'),
         Input(component_id='dd_u_16', component_property='value')]
    )
    def update_fig16(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 17th chart
    @app.callback(
        Output(component_id='g17', component_property='figure'),
        [Input(component_id='dd_r_17', component_property='value'),
         Input(component_id='dd_e_17', component_property='value'),
         Input(component_id='dd_u_17', component_property='value')]
    )
    def update_fig17(*args):
        return update_figure(dfs_multipublish_dict, *args)

    # 18th chart
    @app.callback(
        Output(component_id='g18', component_property='figure'),
        [Input(component_id='dd_r_18', component_property='value'),
         Input(component_id='dd_e_18', component_property='value'),
         Input(component_id='dd_u_18', component_property='value')]
    )
    def update_fig18(*args):
        return update_figure(dfs_multipublish_dict, *args)
