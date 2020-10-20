import databaseconnection
import pandas as pd
from datetime import datetime
import re


# Method which does the data preparation before writing them to the database. 
def prepare_data(filename_complete_path):
    print("Preparing data from the text file.")       
    df = pd.read_csv(filename_complete_path, names = ['CPF', 'Private', 'Incompleto', 'DataUltimaCompra', 'TicketMedio', 'TicketUltimaCompra', 'LojaMaisFrequente', 'LojaUltimaCompra'], 
                        na_filter = True, skiprows=1, delim_whitespace=True)
    df_columns = list(df)
    for column in df_columns:
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('nan', '')
        if column == "TicketMedio" or column == "TicketUltimaCompra": continue
        df[column] = df[column].apply(remove_especial_characteres)
        df[column] = df[column].apply(set_lower_case)
        if column == 'DataUltimaCompra': df[column] = df[column].apply(autoconvert_datetime)
    return df

def remove_especial_characteres(column):
    unaccented_data = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', column)
    return unaccented_data

def set_lower_case(column):
    normalized_data = column.lower()
    return normalized_data

def autoconvert_datetime(value):
    formats = ['%Y-%m-%d']  # formats to try
    result_format = '%Y%m%d'  # output format
    for dt_format in formats:
        try:
            if value == "":
                return value
            dt_obj = datetime.strptime(value, dt_format)
            return dt_obj.strftime(result_format)
        except Exception as e:  # throws exception when format doesn't match
            return value
    return value 