import csv
import six
import os
import sys

def mkdir_safe(dir, msg_if_exist=False):
    """
    Create a directory. If directory already exists, argument used to determine
    whether to raise a warning or just continue.
    
    INPUTS:
    dir - Directory of folder to create
    msg_if_exist - Boolean that asks user to confirm continuing if folder exists (True)
                   or continues without prompt (False)
    """
    if not os.path.exists(dir):
        os.mkdir(dir)
    elif msg_if_exist:
        print('Folder already exists, continue? (y/n)')
        cont = input()
        if cont.lower() != 'y':
            sys.exit("Exiting program...")
        
       
def get_files_ending_with(in_path,extension):
    """
    Writes data to a file.
    
    INPUTS:
    in_path - Input folder 
    extension - File extension
    
    OUTPUTS:
    output_1 - List of file names existing in path with specified extension
    output_2 - List of full file path of files with specified extension in target path
    """
    if os.path.exists(in_path):
        return [f for f in os.listdir(in_path) if f.endswith(extension)], [os.path.join(in_path,f) for f in os.listdir(in_path) if f.endswith(extension)]

    return [], []
    
    
def write_to_file(file_name, data):
    """
    Writes data to a file.
    
    INPUTS:
    file_name - File to write to
    data - Data to write to file. Note if data is of list format, each element is treated as a separate line (but also includes special character behavior)
    """
    with open(file_name, mode="wb") as outfile:
        for line in data:
            outfile.write(str(line))
            outfile.write('\n')
         
         
def write_csv_data(in_file,data,delimiter,write_type):
    """
    Writes csv data to a file. This uses the Python csv package with information at: https://docs.python.org/2.7/library/csv.html.
    
    INPUTS:
    in_file - File to write to
    data - Data to write to file. Expected to be a list format
    delimiter - Delimiter of data (commonly "," or "\t", etc.). For more information visit 
    write_type - How to write data (commonly "wb")
    """
    with open(in_file, write_type) as f:
        writer = csv.writer(f,delimiter=delimiter)
        writer.writerows(data)   

          
def read_csv_data(in_file,delimiter=None):
    """
    Reads csv file to a list. This uses the Python csv package with information at: https://docs.python.org/2.7/library/csv.html.
    
    INPUTS:
    in_file - File to read from
    delimiter - Delimiter of data (commonly "," or "\t", etc.). For more information visit 
    """
    with open(in_file, 'rt') as f:
        if delimiter is not None:
            reader = csv.reader(f,delimiter=delimiter)
        else:
            reader = csv.reader(f)
        my_list = list(reader)
        
    return my_list       
          
          
          