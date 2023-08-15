import configparser
import os
import warnings
import pandas as pd
from config.definitions import ROOT_DIR
# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the settings.ini file
filename = 'Eldora Solar'#'Eldora Solar'#'Trigo Solar'#'BRP Bonete'#'Pecan Praire' #'Big star'
filepath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\' , filename , 'settings.ini')
config.read(filepath)

def main():
    filename = config.get('settings', 'filename')
    casename = config.get('settings', 'SSWG_case')
    loading = int(config.get('settings', 'loading_cutoff'))
    confolder = config.get('settings', 'confolder')
    buses = config.get('settings', 'genbuses')
    SA_county = config.get('settings', 'SA_county')
    dfax_cutoff = float(config.get('settings', 'dfax_cutoff'))
    voltage_cutoff = float(config.get('settings', 'voltage_cutoff'))
    POI_bus = str(config.get('settings', 'POI_bus'))
    level = int(config.get('settings', 'level'))
    #number_of_genbuses = int(config.get('settings', 'number_of_genbuses'))

    #input validation
    #loading
    if type(loading) == int:
        if (0 < loading < 101):
            pass
    else:
        print("Loading cutoff value in settings file is incorrect or out of bounds (0, 100)")

    # confolder matches study case
    if casename == confolder:
        pass
    else:
        print("Casename and Contingency folder names do not match")

    # POI_bus exists in planning data dictionary
    files_folder = os.path.join(ROOT_DIR, 'Input Data\Planning Data Dictionary\\')
    for file in os.listdir(files_folder):
        if file.endswith(".xlsx"):
            plandata = os.path.join(files_folder, file)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(plandata, sheet_name='Data Dictionary', engine="openpyxl")
    if int(POI_bus) in df['SSWG BUS NUMBER'].values:
        pass
    else:
        print("The POI bus number does not exist in the planning data dictionary")

    # Check if gen buses are 6 digit buses
    if len(str([int(bus) for bus in buses.split(',')][0])) == 6:
        pass
    else:
        print("The new generator bus is not a 6 digit number")

    # Check if dfax cutoff value is between 0 and 0.03
    if type(dfax_cutoff) == float:
        if (0 < dfax_cutoff <= 0.03):
            pass
    else:
        print("Dfax cutoff value in settings file is not between 0 and 0.03")

    # Check if voltage cutoff value is between 0 and 0.05
    if type(voltage_cutoff) == float:
        if (0 < voltage_cutoff <= 0.05):
            pass
    else:
        print("Voltage cutoff value in settings file is not between 0 and 0.05")

    print(filename, loading, confolder, buses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level)

    return filename, casename, loading, confolder, buses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level


if __name__ == "__main__":
    main()


