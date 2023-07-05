
import os
from config.definitions import ROOT_DIR
import pyPowerGEM.pyTARA as pt

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
    print('TARA API example case loaded successfully')
    tara.loadRawCase(caseFilePath=case_fp, rawVer=32)
    tara.solveCase()
    for bus in tara.loopBuses():
        print(bus)
    print('TARA API running correctly')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_folderstructure_test()
    tara_test()