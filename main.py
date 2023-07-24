
import os
from config.definitions import ROOT_DIR
import pyPowerGEM.pyTARA as pt
import generatefiles as gf
import TARA_flowgate_screening as tfs
import getcounty as gc
import mapcounty as mc
import Test as tst
import extractGTC as eg

def print_folderstructure_test():
    # Use a breakpoint in the code line below to debug your script.
    print('*******This is a test to check if the code is in correct folder*******')
    print(__file__)
    print('Input folder path:', os.path.join(ROOT_DIR, 'Input Data'))

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
    # input filename, loading percentage, contingency folder name, generator buses and dfax_cutoff
    filename, loading, confolder, buses, SA_county, dfax_cutoff = tst.test()
    # creates con file
    gf.create_combined_confile(ROOT_DIR, filename, confolder)
    # creates mon file
    gf.create_monfile(ROOT_DIR, filename)
    # creates sub file
    gf.create_subfile(ROOT_DIR, filename, buses)
    # Reads con, mon, sub, sswg,
    files = tfs.read_input_files(filename)
    print(files)
    tfs.main(files, loading, dfax_cutoff)
    county = gc.main(filename)
    # merge county obtained from getcounty and extractGTC, then send to map county
    mc.mapcounty(county, SA_county)

