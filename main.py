import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from db_config import *
from transform import *
from output_designer import design_dash

if __name__ == '__main__':
    connection_string = create_connection_string(connection_type, dataportal_db_user, dataportal_db_password,
                                                 dataportal_db_ip, db_port, db_prod_name, db_driver)

    dates = pd.date_range(start='1970-01-01', end='2021-12-31', freq='D')

    df_latest = pd.read_sql(sql_query_latest, connection_string)
    df_prevmonth = pd.read_sql(sql_query_prevmonth, connection_string)

    comb_df_latest = transform_to_combined_dateindex(df_latest, dates)
    comb_df_prevmonth = transform_to_combined_dateindex(df_prevmonth, dates)

    diffpublish_df_dict = {"prev1month" : comb_df_prevmonth, "latest" : comb_df_latest}

    country_list = df_latest['COUNTRY'].unique().tolist()
    distillation_list = df_latest['UNIT_TYPE_DESCRIPTION'].unique().tolist()
    etype_list = df_latest['EVENT_TYPE'].unique().tolist()
    region_list = country_mappings_df['REGION'].unique().tolist()

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
    app.config.suppress_callback_exceptions = True

    design_dash(app, diffpublish_df_dict, region_list, etype_list, distillation_list)

    app.run_server(debug=True)