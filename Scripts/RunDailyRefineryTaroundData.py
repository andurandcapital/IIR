import numpy
import pandas as pd
import sqlalchemy as sa
import os
from ftplib import FTP
global ftp

#pd.set_option('display.max_columns', None)
#DB Details
connection_type = "mssql+pyodbc"
dataportal_db_user = "dataportal"
dataportal_db_password = "FatShamingMarc"
dataportal_db_ip = "10.8.4.35"
db_port = "1433"
db_prod_name = "dataportal_prod"
db_driver = "ODBC+DRIVER+17+for+SQL+Server"
ftp_site='ftp.industrialinfo.com'
user='andurand'
pw='361984'
path = 'C:\\Temp\\IIR\\TAROUND\\'
ftp_path='/data/'
extension='CSV'
filename_pattern='TAROUND'
sql_query = "select distinct(ORIGIN_FILE) from data_iir_offlineevents where origin_file like 'TAROUND%'"

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


def insertTaroundFile(filename, path, connection_string):
    filepath = path + filename
    #Define columns we're interested in from the file
    columns=['DELV_DATE', 'OUTAGE_ID', 'UNIT_NAME', 'UNIT_ID', 'AREA_ID', 'AREA_NAME', 'OWNER_NAME', 'PLANT_ID', 'PLANT_NAME',
             'U_STATUS', 'UTYPE_DESC', 'CHARGERATE', 'CAPACITY', 'TA_START', 'TA_END', 'PRECISION', 'OUTAGE_TYP',
             'OUTAGE_STA', 'OUT_CAUSE', 'PERIOD', 'PAD_DIST', 'COMMENTS']
    renamed_columns={"DELV_DATE": "PUBLISH_DATE", "OUTAGE_ID": "EVENT_ID", "U_STATUS":"UNIT_STATUS",
                 "CHARGERATE":"CAPACITY", "CAPACITY":"CAPACITY_OFFLINE",
                 "TA_START": "EVENT_START", "TA_END": "EVENT_END", "PRECISION": "DATE_PRECISION", "OUTAGE_TYP" : "EVENT_TYPE",
                 "OUTAGE_STA": "EVENT_STATUS", "OUT_CAUSE": "EVENT_CAUSE", "PERIOD" : "EVENT_DURATION", "PAD_DIST": "PAD_DISTRICT"}
    df = pd.read_csv(filepath, low_memory=False)[columns]
    df = df.rename(columns=renamed_columns)
    df["PUBLISH_DATE"] = pd.to_datetime(df["PUBLISH_DATE"], format='%Y%m%d')
    df["EVENT_START"] = pd.to_datetime(df["EVENT_START"], format='%Y%m%d')
    df["EVENT_END"] = pd.to_datetime(df["EVENT_END"], format='%Y%m%d')
    df['ORIGIN_FILE'] = filename
    df.to_sql('data_iir_offlineevents', connection_string, if_exists='append', index=False,
        dtype={ 'PUBLISH_DATE' :   sa.DateTime(),
                'EVENT_ID' :       sa.types.INTEGER(),
                'UNIT_NAME' :     sa.types.VARCHAR(100),
                'UNIT_ID' :       sa.types.INTEGER(),
                'AREA_ID' :       sa.types.INTEGER(),
                'AREA_NAME' :     sa.types.VARCHAR(100),
                'OWNER_NAME' :     sa.types.VARCHAR(100),
                'PLANT_ID' :       sa.types.INTEGER(),
                'PLANT_NAME' :     sa.types.VARCHAR(100),
                'UNIT_STATUS' : sa.types.VARCHAR(30),
                'UTYPE_DESC' : sa.types.VARCHAR(100),
                'CAPACITY' : sa.types.INTEGER(),
                'CAPACITY_OFFLINE' : sa.types.INTEGER(),
                'EVENT_START' :  sa.DateTime(),
                'EVENT_END' :  sa.DateTime(),
                'DATE_PRECISION' : sa.types.VARCHAR(16),
                'EVENT_TYPE' : sa.types.VARCHAR(30),
                'EVENT_STATUS' : sa.types.VARCHAR(30),
                'EVENT_CAUSE' : sa.types.VARCHAR(65),
                'EVENT_DURATION' : sa.types.INTEGER(),
                'PAD_DISTRICT' : sa.types.VARCHAR(65),
                'COMMENTS' : sa.types.VARCHAR(2000),
                'ORIGIN_FILE' : sa.types.VARCHAR(65)})
    print("File %s uploaded successfully to the database" % filename)


connection_string = create_connection_string(connection_type,dataportal_db_user,dataportal_db_password,dataportal_db_ip,db_port,db_prod_name, db_driver)
current_files = [file.upper() for file in pd.read_sql(sql_query, connection_string)["ORIGIN_FILE"]]

# Download missing files and save to db
ftp = FTP(ftp_site, user=user, passwd=pw)
ftp.cwd(ftp_path)
file_names = [fn.upper() for fn in ftp.nlst()
              if filename_pattern in fn.upper() and fn.upper().endswith(extension) and fn.upper() not in current_files]
for file_name in file_names:
    local_filename = os.path.join(path, file_name)
    if not os.path.isfile(local_filename):
        with open(local_filename, 'wb') as local_file:
            ftp.retrbinary('RETR %s' % file_name, local_file.write)
            print("Downloaded: %s" % file_name);
    else:
        print("File already exists on drive");

    insertTaroundFile(file_name, path, connection_string)

