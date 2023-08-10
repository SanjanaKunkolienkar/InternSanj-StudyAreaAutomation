# get output of all counties (red+blue) and (red+blue+green); only buses selected in counties - input to this function

from config.definitions import ROOT_DIR
import warnings
import os
import pandas as pd
import extractbuses as eb
import getcounty as gc
import psse_get_data as getdata
import openpyxl
from openpyxl.styles import NamedStyle, Font, PatternFill

def generate_dashboard(county_flip, county, buses_nl_v_dfax, filename):
    county_blue = county_flip
    county_red = county


    buses_red = eb.extract_from_counties(county_red)
    buses_blue = eb.extract_from_counties(county_blue)

    buses_red_blue = buses_red + buses_blue
    #Calculating data for buses that are sensitive
    bus_df_sensitive = getdata.main(filename, buses_nl_v_dfax)
    total_gen_s = bus_df_sensitive['Gen MVA'].sum()
    total_load_s = bus_df_sensitive['Bus MVA'].sum()
    tran_buses_s = bus_df_sensitive['Type'].value_counts()[float(1)]
    gen_buses_s =  bus_df_sensitive['Type'].value_counts()[float(2)]

    dash_data_s = [['Total Generation "Capacity" (units)', total_gen_s], ['Total Load (units)', total_load_s],
                   ['Total Number of Transmission Buses', tran_buses_s],
                   ['Total Number of Generation Buses', gen_buses_s]]
    dash_df_s = pd.DataFrame(dash_data_s, columns=['Dashboard', ''])
    dash_df_s.set_index('Dashboard')



    # Calculating data for all buses
    bus_df_red_blue = getdata.main(filename, buses_red_blue)
    total_gen_a = bus_df_red_blue['Gen MVA'].sum()
    total_load_a = bus_df_red_blue['Bus MVA'].sum()
    tran_buses_a = bus_df_red_blue['Type'].value_counts()[float(1)]
    gen_buses_a = bus_df_red_blue['Type'].value_counts()[float(2)]

    dash_data_a = [['Total Generation "Capacity" (units)', total_gen_a], ['Total Load (units)', total_load_a],
                   ['Total Number of Transmission Buses', tran_buses_a],
                   ['Total Number of Generation Buses', gen_buses_a]]
    dash_df_a = pd.DataFrame(dash_data_a, columns=['Dashboard', ''])
    dash_df_a.set_index('Dashboard')



    filepath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Temp_Dash.xlsx')
    with pd.ExcelWriter(filepath) as writer:
        bus_df_sensitive.to_excel(writer, startcol=0, startrow=10, sheet_name='Sheet1')
        dash_df_s.to_excel(writer, startcol=0, startrow=1, sheet_name='Sheet1')
        bus_df_red_blue.to_excel(writer, startcol=0, startrow=10, sheet_name='Sheet2')
        dash_df_a.to_excel(writer, startcol=0, startrow=1, sheet_name='Sheet2')


    #Change sheet names to indicate sensitive buses and all buses in red + blue
    workbook_1 = writer.book
    #workbook_1 = xlrd.open_workbook(filepath)
    all_sheets = writer.sheets# Adding formats for header row.
    # Create a named style for the header
    header_style = NamedStyle(name="header_style")
    header_style.font = Font(name="Tahoma", size=16, color="00339966", bold=True)  # Set font to bold
    # Create a pattern fill for the background color (green)
    fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
    header_style.fill = fill

    for sheet in all_sheets:
        # change the sheet title
        if sheet.title == 'Sheet1':
            sheet.title = 'Sensitive Buses'# Apply the header style to the specified header row
            for cell in sheet[B10]:
                cell.style = header_style
        if sheet.title == 'Sheet2':
            sheet.title = 'All buses'
            for cell in sheet[11]:
                cell.style = header_style

def missing_gen():
    pass
def main():
    generate_dashboard(county_flip, county, buses_nl_v_dfax, filename)

if __name__ == "__main__":
    main()