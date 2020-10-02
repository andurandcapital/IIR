
# DB Details
connection_type = "mssql+pyodbc"
dataportal_db_user = "dataportal"
dataportal_db_password = "FatShamingMarc"
dataportal_db_ip = "10.8.4.35"
db_port = "1433"
db_prod_name = "dataportal_prod"
db_driver = "ODBC+DRIVER+17+for+SQL+Server"

sql_query_prevmonth = "select * from udf_data_iir_offlineevents_unique_latest(dateadd(MONTH, -1, getdate()))"
sql_query_latest = "select * from data_iir_offlineevents_unique_latest_v"

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