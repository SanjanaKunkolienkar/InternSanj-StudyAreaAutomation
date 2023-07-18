import os
def create_combined_confile(ROOT_DIR, filename, confolder):
    # Function to combine all ERCOT confiles : only includes N-1 contingencies: P1, P2, P4, P5 and P7
    path_to_file = os.path.join(ROOT_DIR, 'Input Data\ERCOTcontingencies\\', confolder)
    output_file = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'files\\')
    print(output_file)
    opfilename = os.path.join(output_file, 'AllERCOTcontingencies.con')
    with open(opfilename, 'w') as f:
        f.write('DEFAULT DISPATCH\n  SUBSYSTEM \'Export\'\nEND\n')
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
def create_monfile(ROOT_DIR, filename):
    output_file = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'files\\')
    filename = os.path.join(output_file, 'MON.mon')
    with open(filename, 'w') as f:
        f.write('MONITOR BRANCHES IN SUBSYSTEM \'Import\'\n')
        f.write('MONITOR VOLTAGE RANGE IN SUBSYSTEM \'Import\'  0.92 1.050\n')
        f.write('MONITOR VOLTAGE DEVIATION IN SUBSYSTEM \'Import\'  0.080 0.080\n')
        f.write('MONITOR TIES FROM SUBSYSTEM \'Import\'\n')
        f.write('\nEND')

def create_subfile(ROOT_DIR, filename, buses):
    inputbuses = buses #input("Enter the study buses to which generators are connected in the following format XXXXXX, XXXXXX : ")
    buses = [int(bus) for bus in inputbuses.split(",")]
    output_file = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'files\\')
    filename = os.path.join(output_file, 'SUB.sub')
    with open(filename, 'w') as f:
        f.write('subsystem \'Export\'\n')
        for bus in buses:
            statement = '{}{}{}'.format(' bus ', bus, '\n')
            f.write(statement)
        f.write('End\n')
        f.write('subsystem \'Import\'\n')
        f.write(' AREAS 1 1200\n') #assuming all SSWG cases have Areas 1 to 1200
        f.write(' scale all for Import\n')
        f.write('End\n')