import os,sys,shutil
import pandas as pd
from config.definitions import ROOT_DIR
import getcounty as gc

def extractGTC(studycounty):
    #extract all buses from GTC document
    cwd = os.path.join(ROOT_DIR, 'Input Data\GTCList\\')
    for file in os.listdir(cwd):
        if file.endswith(".xlsm"):
            gtclist = os.path.join(cwd, file)

    gtc_interface_name = pd.read_excel(gtclist, 'Summary', skiprows=7)
    skip = {
        'N_TO_H' : 20,
        'VALIMP' : 20,
        'PNHNDL' : 22,
        'WESTEX' : 30,
        'MCCAMY' : 18,
        'NELRIO' : 16,
        'REDTAP' : 15,
        'EASTEX' : 20,
        'TRDWEL' : 16,
        'RV_RH' : 18,
        'BEARKT': 16,
        'VALEXP': 20,
        'ZAPSTR': 16,
        'CULBSN': 18,
        'WILBRN': 17,
        'WHARTN': 18,
        'HMLTN': 16,
    } #'NE_LOB' : 7,

    buses = []
    for interface_name in gtc_interface_name['Interface name']:
        df = pd.read_excel(gtclist, sheet_name=interface_name, skiprows=skip[interface_name])
        buses.extend(df['From Bus Number (SSWG)'].tolist())
        buses.extend(df['To Bus Number (SSWG)'].tolist())
    bus = [x for x in buses if x == x] #remove nan
    buses=[]
    buses = [int(x) for x in bus]
    unique_buses = [*set(buses)] #get unique buses from the list
    #get a list of counties corresponding to these buses
    countylist = [*set(gc.getcounty(unique_buses))]
    #read the county adjacency excel
    adjfile = os.path.join(ROOT_DIR, 'Input Data\TexasCountyMap\county_adjacency2010.csv')
    adj_county = pd.read_csv(adjfile)
    texas_adj_county = adj_county[adj_county['countyname'].str.contains(', TX')]
    # check for GTC counties 2 levels away from study county
    #return county list around SA - 1 county away
    SA_adj_county_list = []
    SA_adj_county_list_final = []
    # counties that are around the study county
    studycounty_adj = texas_adj_county[texas_adj_county['countyname'].str.contains(studycounty)]
    SA_adj_county_list.extend(studycounty_adj['neighborname'].tolist())
    print(SA_adj_county_list)
    SA_adj_county_list_final = SA_adj_county_list
    #find counties that are around the study county
    n=0
    for county in SA_adj_county_list:
        print(county)
        #print(county)
        county_adj = texas_adj_county[texas_adj_county['countyname'].str.contains(county)]
        SA_adj_county_list_final.extend(county_adj['neighborname'].tolist())
        #print(SA_adj_county_list_final)
        n=n+1

if __name__ == '__main__':
    studycounty = 'Leon'
    extractGTC(studycounty)