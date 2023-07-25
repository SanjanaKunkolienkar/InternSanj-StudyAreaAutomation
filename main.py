
import os
from config.definitions import ROOT_DIR
import pyPowerGEM.pyTARA as pt
import generatefiles as gf
import TARA_flowgate_screening as tfs
import getcounty as gc
import mapcounty as mc
import Test as tst
import extractGTC as eg
import PSSE_model_details as ps

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
    ## tara_test()
    # input filename, loading percentage, contingency folder name, generator buses and dfax_cutoff
    filename, loading, confolder, buses, SA_county, dfax_cutoff, voltage_cutoff = tst.test()
    # creates con file - function name: generatefiles.py
    gf.create_combined_confile(ROOT_DIR, filename, confolder)
    # creates mon file - function name: generatefiles.py
    gf.create_monfile(ROOT_DIR, filename)
    # creates sub file - function name: generatefiles.py
    gf.create_subfile(ROOT_DIR, filename, buses)
    # reads con, mon, sub, sswg and create sub-directory to store results
    files = tfs.read_input_files(filename)
    # run TARA flowgate screening
    tfs.main(files, loading, dfax_cutoff)
    county1 = gc.main(filename)
    county2 = ps.main(filename, voltage_cutoff, [])
    county = county1 + county2
    county = [*set(county)]
    # merge county obtained from getcounty and extractGTC, then send to map county
    mc.mapcounty(county, SA_county)

