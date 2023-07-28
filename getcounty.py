import os
import pandas as pd
import numpy as np
from config.definitions import ROOT_DIR
import extractbuses as eb
import warnings


def getcounty(buses, POI):
    files_folder = os.path.join(ROOT_DIR, 'Input Data\Planning Data Dictionary\\')
    for file in os.listdir(files_folder):
        if file.endswith(".xlsx"):
            plandata = os.path.join(files_folder, file)

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        df = pd.read_excel(plandata, sheet_name='Data Dictionary', engine="openpyxl")

    check_bus = "All buses accounted for"
    county_list = []
    missing_list= []
    sa_county = df.loc[df['SSWG BUS NUMBER'] == POI, 'PLANNING BUS COUNTY'].item()
    print('STUDY County', sa_county)
    for bus in buses:
        if bus in df['SSWG BUS NUMBER'].values:
            county = df.loc[df['SSWG BUS NUMBER'] == bus, 'PLANNING BUS COUNTY'].item()
            county_list.append(county)
        else:
            check_bus = "Bus is missing from planning dictionary. Check if these are from the study system: \n"
            missing_list.append(bus)
    county_list = [*set(county_list)]
    cleanedList = [x for x in county_list if x == x]

    if sa_county == 'REYNOSA':
        sa_county = 'HIDALGO'

    print(county_list)
    print(check_bus, missing_list)
    return cleanedList, sa_county

def main(filename, POI):
    buses = eb.main(filename)
    cl, sa_county = getcounty(buses, POI)
    return cl, sa_county

# if __name__ == "__main__":
#     filename = 'BRP Bonete'
#     main(filename)
