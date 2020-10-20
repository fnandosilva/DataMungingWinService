from watchdog.observers import Observer
import time 
from watchdog.events import FileSystemEventHandler
import os
import json
import unicodedata
import databaseconnection
import pandas as pd
import time
import logging
from datetime import datetime
from cnpj import Cnpj
from cpf import Cpf
import filedatamanipulation as fdm

# coding = utf-8

class FileDataHandler(FileSystemEventHandler):

    """ This is the class which inherits the FileSystemEventHandler
        class. For this class, we'are going to handle data prep and 
        insert the data from a text file to Sql database table
    """

    # The event method which whatches text files (.csv or .txt)
    def on_modified(self, event):
       logging.basicConfig(filename = r'C:\Files\ErrorLog\erros.Log', level = logging.DEBUG)
       logger = logging.getLogger()
       start_time = time.time()

       i = 1

       new_filename = "processed_file" + str(i) + ".txt"
       
       try:
           for filename in os.listdir(folder_to_track):
               filename_complete_path = folder_to_track + "/" + filename
               dataframe = fdm.prepare_data(filename_complete_path)
               databaseconnection.create_table_CustomersPurchase()
               databaseconnection.insert_into_table_CustomersPurchase(dataframe)
               file_exists = os.path.isfile(folder_destination + "/" + new_filename)
               while file_exists:
                   i += 1
                   new_filename = "processed_file" + str(i) + ".txt"
                   file_exists = os.path.isfile(folder_destination + "/" + new_filename)
               src = folder_to_track + "/" + filename
               new_destination = folder_destination + "/" + new_filename
               print("Moving file from Files folder to ProcessedFiles folder")
               os.rename(src, new_destination)
               execution_stop_time = time.time()
               execution_dt = execution_stop_time - start_time
               print("Program successfully executed in:", execution_dt)
       except Exception as e:
           print("An error has occured:", e)
           logger.error(e)
       finally:
           stop_time = time.time()
           dt = stop_time - start_time
           logger.info('Time required for {file} = {time}'.format(file=filename, time=dt))

if __name__ == "__main__":
    # It stabilishes the base of FileDataHandler in addition folder to be tracked and folder destination
    # Verify if the folder_to_track and folder_destination are created if not it creates them all
    folder_to_track = r'C:\Files'
    folder_destination = r'C:\Files\ProcessedFiles'
    folder_errorlog = r'C:\Files\ErrorLog'

    if not os.path.exists(folder_to_track):
        os.makedirs(folder_to_track)
    if not os.path.exists(folder_destination):
        os.makedirs(folder_destination)
    if not os.path.exists(folder_errorlog):
        os.makedirs(folder_errorlog)

    # Initialize FileDataHandler and Observer event
    event_handler = FileDataHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()