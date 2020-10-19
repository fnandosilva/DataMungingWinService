from watchdog.observers import Observer
import time 
from watchdog.events import FileSystemEventHandler
import os
import json
import unicodedata
import re
import databaseconnection
import pandas as pd
from datetime import datetime
from cnpj import Cnpj
from cpf import Cpf

encoding = "utf-8"

class FileDataHandler(FileSystemEventHandler):

    """ This is the class which inherits the FileSystemEventHandler
        class. For this class, we'are going to handle data prep and 
        insert the data from a text file to Sql database table
    """

    i = 1

    # The event method which whatches text files (.csv or .txt)
    def on_modified(self, event):

       new_filename = "processed_file" + str(self.i) + ".txt"

       try:

           for filename in os.listdir(folder_to_track):
               filename_complete_path = folder_to_track + "/" + filename

               dataframe = self.prepare_data(filename_complete_path)
               databaseconnection.create_table_CustomersPurchase()
               databaseconnection.insert_into_table_CustomersPurchase(dataframe)

               file_exists = os.path.isfile(folder_destination + "/" + new_filename)

               while file_exists:
                   self.i += 1
                   new_filename = "processed_file" + str(self.i) + ".txt"
                   file_exists = os.path.isfile(folder_destination + "/" + new_filename)
               src = folder_to_track + "/" + filename
               new_destination = folder_destination + "/" + new_filename
               print("Moving file from Files folder to ProcessedFiles folder")
               os.rename(src, new_destination)
               print("Program successfully executed!")

       except Exception as e:
           print("An error has occured:", e)

    # Method which does the data preparation before writing them to the database. 
    def prepare_data(self, filename_complete_path):
        print("Preparing data from the text file.")       
        df = pd.read_csv(filename_complete_path, names = ['CPF', 'Private', 'Incompleto', 'DataUltimaCompra', 'TicketMedio', 'TicketUltimaCompra', 'LojaMaisFrequente', 'LojaUltimaCompra'], 
                         na_filter = True, skiprows=1, delim_whitespace=True)
        df_columns = list(df)
        for column in df_columns:
            df[column] = df[column].astype(str)
            df[column] = df[column].str.replace('nan', '')
            if column == "TicketMedio" or column == "TicketUltimaCompra": continue
            df[column] = df[column].apply(self.remove_especial_characteres)
            df[column] = df[column].apply(self.set_lower_case)
            if column == 'DataUltimaCompra': df[column] = df[column].apply(self.autoconvert_datetime)
        return df

    def remove_especial_characteres(self, column):
        unaccented_data = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', column)
        return unaccented_data

    def set_lower_case(self, column):
        normalized_data = column.lower()
        return normalized_data

    def autoconvert_datetime(self, value):
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

# It stabilishes the base of FileDataHandler in addition folder to be tracked and folder destination
# Verify if the folder_to_track and folder_destination are created if not it creates them all
folder_to_track = r'C:\Files'
folder_destination = r'C:\Files\ProcessedFiles'

if not os.path.exists(folder_to_track):
    os.makedirs(folder_to_track)
if not os.path.exists(folder_destination):
    os.makedirs(folder_destination)

# Initialize FileDataHandler and Observer event
event_handler = FileDataHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
observer.join()