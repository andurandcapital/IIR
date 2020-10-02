import plotly.graph_objects as go

# Creates a list of dictionaries, which have the keys 'label' and 'value'. (used in dcc.Dropdown below)
def get_dropdown_options(list_params):
    dict_list = []
    for i in list_params:
        dict_list.append({'label': i, 'value': i})

    return dict_list


# function for creating graphs to apply to each callback
def update_figure(diffpublish_df_dict, selected_dropdown_region, selected_planning_type, selected_distillation_type):

    trace = []
    # draw and append traces for each country
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years_2 = [2019, 2020]
    years_5 = [2016, 2017, 2018, 2019, 2020]


    for region, planning_type, distillation_type in zip(selected_dropdown_region,selected_planning_type, selected_distillation_type):
        # 2019 & 2020
        for year in years_2:
            trace.append(go.Scatter(x= months,
                                    y= diffpublish_df_dict['latest'].loc[year,(region, planning_type, distillation_type)],
                                    mode = 'lines + markers',
                                    line_shape='spline',
                                    name = year))
        # as of 1 month ago
        trace.append(go.Scatter(x=months,
                                y=diffpublish_df_dict['prev1month'].loc[2020, (region, planning_type, distillation_type)],
                                mode='lines + markers',
                                line_shape='spline',
                                name='1 month ago'))

        # Draw 5 year average
        trace.append(go.Scatter(x=months,
                                y=diffpublish_df_dict['latest'].loc[years_5, (region, planning_type, distillation_type)]
                                .mean(axis=0,level='MONTH'),
                                mode='lines + markers',
                                line_shape='spline',
                                name='5yr avg'))

    traces = [trace]
    data = [val for sublist in traces for val in sublist]

    # define figure for graph output
    layout = go.Layout(colorway=['#17becf', '#e377c2', '#ff7f0e', '#2ca02c', 'black', 'grey'],
                       title={'text': ' '},
                       margin={'t': 40, 'b': 40, 'l': 40, 'r': 10},
                       legend=dict(orientation='h', yanchor="bottom", y=-0.25, xanchor="left", x=0))
    figure = {'data': data, 'layout': layout}

    return figure


