##### This function is not called anywhere yet and is for future purpose of adding missing generators to the dashboard ######


from config.definitions import ROOT_DIR
import warnings
import os
import pandas as pd


def get_missing_gen(filename, county, county_flip):
    study_area = set(county) | set(county_flip)
    filepath = os.path.join(ROOT_DIR,
                            'Input Data\Missing Gen Files\Generation Dispatch_per GIS June-2023_07172023v2.xlsx')
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        GIS_wind_solar_data = pd.read_excel(filepath, sheet_name='Proposed Wind&Solar with IA', header=1, engine="openpyxl")
        GIS_BESS_data = pd.read_excel(filepath, sheet_name='BESS Projects with IA', header=1, engine="openpyxl")
        GIS_conv_data = pd.read_excel(filepath, sheet_name='Conventional Projects with IA', header=1, nrows=35, engine="openpyxl")
        GIS_smallgen_data = pd.read_excel(filepath, sheet_name='Small Gen Projects', header=1, nrows=24,  engine="openpyxl")

    # Filter Data based on Meet requirements of 6.9
    GIS_wind_solar_data = GIS_wind_solar_data[
        GIS_wind_solar_data['Meets Section 6.9 Requirements (1)(b) through (1)(d)'] == 'Yes']
    GIS_BESS_data = GIS_BESS_data[GIS_BESS_data['Meets Section 6.9 Requirements (1)(b) through (1)(d)'] == 'Yes']
    GIS_conv_data = GIS_conv_data[GIS_conv_data['Meets Section 6.9 Requirements (1)(b) through (1)(d)'] == 'Yes']

    # Filter Data based on Meet requirements of 6.9
    GIS_wind_solar_data = GIS_wind_solar_data[GIS_wind_solar_data['Remarks'] != 'Inactive']
    GIS_BESS_data = GIS_BESS_data[GIS_BESS_data['Remarks'] != 'Inactive']
    GIS_conv_data = GIS_conv_data[GIS_conv_data['Remarks'] != 'Inactive']
    GIS_smallgen_data = GIS_smallgen_data[GIS_smallgen_data['Remarks'] != 'Inactive']

    # Filter Data based on county
    GIS_wind_solar_data = GIS_wind_solar_data[GIS_wind_solar_data['County'].str.lower().isin(study_area)]
    GIS_BESS_data = GIS_BESS_data[GIS_BESS_data['County'].str.lower().isin(study_area)]
    GIS_conv_data = GIS_conv_data[GIS_conv_data['County'].str.lower().isin(study_area)]
    GIS_smallgen_data = GIS_smallgen_data[GIS_smallgen_data['County'].str.lower().isin(study_area)]

    GIS_gen_list = pd.DataFrame(columns=['Bus Number', 'Nameplate Capacity (MW)', 'County'])
    if GIS_wind_solar_data.empty:
        print("DataFrame is empty")
    else:
        GIS_gen_list = GIS_gen_list._append(GIS_wind_solar_data[['Bus Number', 'Nameplate Capacity as per GIS (MW)',
                                                                 'County', 'POI Location as per GIS Report']],
                                            ignore_index=True)
    if GIS_BESS_data.empty:
        print("DataFrame is empty")
    else:
        GIS_gen_list = GIS_gen_list._append(GIS_BESS_data[['Bus Number', 'Nameplate Capacity as per GIS (MW)',
                                                           'County', 'POI Location as per GIS Report']],
                                            ignore_index=True)

    if GIS_conv_data.empty:
        print("DataFrame is empty")
    else:
        GIS_gen_list = GIS_gen_list._append(GIS_conv_data[['Bus Number', 'Nameplate Capacity as per GIS (MW)',
                                                           'County', 'POI Location as per GIS Report']],
                                            ignore_index=True)

    if GIS_smallgen_data.empty:
        print("DataFrame is empty")
    else:
        GIS_gen_list = GIS_gen_list._append(GIS_smallgen_data[['Bus Number', 'Nameplate Capacity as per GIS (MW)',
                                                               'County', 'POI Location']], ignore_index=True)

    if GIS_gen_list.empty:
        print("DataFrame is empty")
    else:
        GIS_gen_list.to_csv(os.path.join(ROOT_DIR,'Input Data\Missing Gen Files\GIS_gen_list.csv'))

    # print(GIS_wind_solar_data)
    # print(GIS_BESS_data)
    # print(GIS_conv_data)
    # print(GIS_smallgen_data)



