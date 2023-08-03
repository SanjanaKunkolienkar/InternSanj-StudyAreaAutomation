import os
import pandas as pd
from config.definitions import ROOT_DIR
import warnings

#Initially it extracts buses from flowgates and sends to get counties
def extract_from_fg_violations(filename):

    filepath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename , 'Temp\FilteredFlowgates.csv')
    viol = (pd.read_csv(filepath, skiprows=10)).iloc[:,1]
    buses = []
    print(viol.head())
    for num in viol:
        words = (num.strip()).split(" ")
        #print(words)
        filtered = filter(lambda x: (len(x) > 0) and (len(x) < 7), words)
        filtered_list = list(filtered)
        #print(filtered_list[0])
        word = [x for x in filtered_list if ((x == '-') or (x.isdigit())) and ((x != '138') and (x != '345') and (x != '1'))]
        #print(word)
        buses.append(int(word[0]))
        buses.append(int(word[1]))

    unique_buses = [*set(buses)]
    #print(len(buses))
    print(unique_buses)
    return unique_buses

def extract_from_counties(countylist):
    files_folder = os.path.join(ROOT_DIR, 'Input Data\Planning Data Dictionary\\')
    for file in os.listdir(files_folder):
        if file.endswith(".xlsx"):
            plandata = os.path.join(files_folder, file)

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(plandata, sheet_name='Data Dictionary', engine="openpyxl")

    buses = []
    for county in countylist:
        val = df.loc[df['PLANNING BUS COUNTY'].str.lower() == county.lower(), 'SSWG BUS NUMBER'].tolist()
        buses.append(val)

    flat_list = [item for sublist in buses for item in sublist] #converting a list of lists to a flat list
    unique_buses = [*set(flat_list)] #eliminating repetitive bus numbers
    return unique_buses
def main(filename):
    action = 'flowgatescreening'
    if action == 'flowgatescreening':
        buses = extract_from_fg_violations(filename)
        return buses
