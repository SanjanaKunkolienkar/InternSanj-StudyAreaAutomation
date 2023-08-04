
from config.definitions import ROOT_DIR
import pyPowerGEM.pyTARA as pt
import generatefiles as gf
import TARA_flowgate_screening as tfs
import getcounty as gc
import mapcounty as mc
import Test as tst
import voltagesensitivity as vs
import nlevels as nl
import extractbuses as eb
import read_user_input as read


def tara_test():
    # This function checks if access to TARA is available on your computer
    # before v2002.1 the python DLL is required
    tara = pt.taraAPI(dllFilePath=r'P:\TARA\API\tara.dll')
    # after v2002.1 the DLL is optional, API uses the installed DLL
    tara = pt.taraAPI()
    #Load example case
    print('TARA API loading case')
    case_fp = r'P:\TARA\API\examples\pyTARA\example_data\sample2014.raw'
    tara.loadRawCase(caseFilePath=case_fp, rawVer=32)
    print('TARA API example case loaded successfully')
    tara.solveCase()
    for bus in tara.loopBuses():
        print(bus)
    print('TARA API running correctly')
    # Press the green button in the gutter to run the script.

if __name__ == '__main__':
    # check if TARA runs on your system
    tara_test()

    # replaced with user input file as a .ini file
    filename, loading, confolder, genbuses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level = read.main() #tst.test()

    #Get counties that are N-levels away
    county_nlevels = nl.main(filename, POI_bus, level, SA_county)
    county_final = set([SA_county.lower()]) | set(county_nlevels) #Combine study county with counties n-levels away
    county = [*set(county_final)]
    print("Counties", county)

    # map counties obtained from (previous step + convex hull of counties from previous step)
    county_hull = mc.main(county, SA_county) #returns a list of counties

    #get all buses in these counties
    buses = eb.extract_from_counties(county_hull)

    #### Create mon, con and sub files for running TARA ####
    # creates con file - function name: generatefiles.py
    gf.create_combined_confile(ROOT_DIR, filename, confolder)
    # creates mon file - function name: generatefiles.py
    gf.create_monfile(ROOT_DIR, filename)
    # creates sub file - function name: generatefiles.py
    gf.create_subfile(ROOT_DIR, filename, buses, genbuses)


    # reads con, mon, sub, sswg and create sub-directory to store results
    files = tfs.read_input_files(filename)
    # run TARA flowgate screening
    tfs.main(files, loading, dfax_cutoff)
    county_dfax = gc.main(filename, SA_county)
    county_voltage = vs.main(filename, voltage_cutoff, SA_county, buses)

    print(county_voltage)

    county_flip = (set(county_dfax) | set(county_voltage)) - set(county)

    print(county_flip)

    mc.map_study_area(county, county_flip, SA_county)

    # # county2 = vs.main(filename, voltage_cutoff, SA_county)
    #
    # # print("County 1, 2 and 3")
    # # print(county1)
    # # print(county2)
    #
    # # merge county obtained from getcounty and extractGTC, then send to map county


