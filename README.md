# DataMungingWinService

This project was built as a service which manipulates text files data and writes to a SQL database table.

In the DataMunging we have all scripts used to develop this service.

In this folder there is a executable file named datamungingwinservice.exe. Once, double-clicked on this executable file the service is going to be running behind the scenes.

It is going to create a folder called Files on the path "C:" which is going to be processed text files. Also, inside folder Files is going to be created two other files called ProcessedFiles and ErrorLog. The ProcessedFiles is the folder that keeps all processed and moved files from folder Files. The ErrorLog is the folder that keeps the error file with all processing errors from the service.

All text files should be pasted on folder Files to be processed. Once, this file is pasted the service will be executed and the file will be moved to folder ProcessedFiles. You must first start the service before pasting a file on the folder named Files. To make sure the data munging service is running you must go to the universal path "C:" and see if service created the two folders "Files" and "ProcessedFiles".
