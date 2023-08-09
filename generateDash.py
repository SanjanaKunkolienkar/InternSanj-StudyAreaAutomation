# get output of all counties (red+blue) and (red+blue+green); only buses selected in counties - input to this function

from config.definitions import ROOT_DIR
import warnings
import os
import pandas as pd
import extractbuses as eb
import getcounty as gc


def generate_dashboard(SA_county, county_flip, county, buses_nl_v_dfax, filename):
    county_blue = county_flip
    county_red = county


    buses_red = eb.extract_from_counties(county_red)
    buses_blue = eb.extract_from_counties(county_blue)

    buses_red_blue = buses_red + buses_blue
    bus_df_sensitive = determine_gen(buses_nl_v_dfax)
    buses_df_red_blue = determine_gen(buses_red_blue)

    filepath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Temp_Dash.xlsx')
    with pd.ExcelWriter(filepath) as writer:
        bus_df_sensitive.to_excel(writer, sheet_name='Sheet1')
        buses_df_red_blue.to_excel(writer, sheet_name='Sheet2')




def determine_gen(bus_list):
    bus_df = pd.DataFrame(columns=['Bus Number', 'Type'])
    for bus in bus_list:
        if len(str(bus)) == 6:
            df_temp = {'Bus Number': bus, 'Type': 'Generator'}
            bus_df = bus_df._append(df_temp, ignore_index = True)
        else:
            df_temp = {'Bus Number': bus, 'Type': 'Not Generator'}
            bus_df = bus_df._append(df_temp, ignore_index=True)

    return bus_df


def main():
    generate_dashboard(SA_county, county_flip, county, buses_nl_v_dfax, filename)

if __name__ == "__main__":
    main()