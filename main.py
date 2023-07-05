
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

def create_combined_confile():
    # Function to combine all ERCOT confiles : only includes N-1 contingencies: P1, P2, P4, P5 and P7
    path_to_file = os.path.join(ROOT_DIR, 'Input Data\ERCOTcontingencies\\')
    output_file = os.path.join(ROOT_DIR, 'Temp\\')
    filename = os.path.join(output_file, 'AllERCOTcontingencies.con')
    with open(filename, 'w') as f:
        f.write('DEFAULT DISPATCH\n  SUBSYSTEM \'DEFAULT DISPATCH\'\nEND\n')
        f.write('')
        f.write('/ *Contingencies in P1\n')
        f.write('CONTINGENCY_TYPE\n  SET TYPES Type\n  SET VALUES P1\nEND\n')
        for file in os.listdir(path_to_file):
            if '_P1.' in file:
                statement = 'INCLUDE \"'+os.path.join(path_to_file,file)+'\"'
                f.write(statement)
                f.write('\n')
        f.write('/ *Contingencies in P2\n')
        f.write('CONTINGENCY_TYPE\n  SET TYPES Type\n  SET VALUES P2\nEND\n')
        for file in os.listdir(path_to_file):
            if '_P2.' in file:
                statement = 'INCLUDE \"' + os.path.join(path_to_file, file) + '\"'
                f.write(statement)
                f.write('\n')
        f.write('/ *Contingencies in P4\n')
        f.write('CONTINGENCY_TYPE\n  SET TYPES Type\n  SET VALUES P4\nEND\n')
        for file in os.listdir(path_to_file):
            if '_P4.' in file:
                statement = 'INCLUDE \"' + os.path.join(path_to_file, file) + '\"'
                f.write(statement)
                f.write('\n')
        f.write('/ *Contingencies in P5\n')
        f.write('CONTINGENCY_TYPE\n  SET TYPES Type\n  SET VALUES P5\nEND\n')
        for file in os.listdir(path_to_file):
            if '_P5.' in file:
                statement = 'INCLUDE \"' + os.path.join(path_to_file, file) + '\"'
                f.write(statement)
                f.write('\n')
        f.write('/ *Contingencies in P7\n')
        f.write('CONTINGENCY_TYPE\n  SET TYPES Type\n  SET VALUES P7\nEND\n')
        for file in os.listdir(path_to_file):
            if '_P7.' in file:
                statement = 'INCLUDE \"' + os.path.join(path_to_file, file) + '\"'
                f.write(statement)
                f.write('\n')

if __name__ == '__main__':
    print_folderstructure_test()
    tara_test()
    create_combined_confile()