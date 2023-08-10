from config.definitions import ROOT_DIR
import os, sys
import numpy as np
import pandas as pd
import getcounty as gc


def bus_vals(bus):


    return bus_type
def main(filename, buses):
    cwd = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename)
    for file in os.listdir(os.path.join(cwd, 'Study Case')):
        if file.endswith(".raw"):
            study_file = os.path.join(cwd, 'Study Case', file)

    if os.path.exists("C:\\Program Files\\PTI\\PSSE35\\35.3\\PSSBIN"):
        sys.path.insert(0, "C:\\Program Files\\PTI\\PSSE35\\35.3\\PSSBIN")
        os.environ['PATH'] = "C:\\Program Files\\PTI\\PSSE35\\35.3\\PSSBIN" + ";" + os.environ['PATH']
        sys.path.insert(0, "C:\\Program Files\\PTI\\PSSE35\\35.3\\PSSPY39")
        os.environ['PATH'] = "C:\\Program Files\\PTI\\PSSE35\\35.3\\PSSPY39" + ";" + os.environ['PATH']
    elif os.path.exists("C:\\Program Files (x86)\\PTI\\PSSE35\\35.3\\PSSBIN"):
        sys.path.insert(0, "C:\\Program Files (x86)\\PTI\\PSSE35\\35.3\\PSSBIN")
        os.environ['PATH'] = "C:\\Program Files (x86)\\PTI\\PSSE35\\35.3\\PSSBIN" + ";" + os.environ['PATH']
        sys.path.insert(0, "C:\\Program Files (x86)\\PTI\\PSSE35\\35.3\\PSSPY39")
        os.environ['PATH'] = "C:\\Program Files (x86)\\PTI\\PSSE35\\35.3\\PSSPY39" + ";" + os.environ['PATH']

    import psse35
    import psspy
    import redirect
    _i = psspy.getdefaultint()
    _f = psspy.getdefaultreal()
    _s = psspy.getdefaultchar()

    redirect.psse2py()
    ierr = psspy.psseinit(150000)
    psspy.lines_per_page_one_device(1, 100000)

    if study_file.endswith(".raw"):
        psspy.read(0, study_file)

    bus_df = pd.DataFrame(columns =['Bus Number', 'Type', 'Bus MVA', 'Gen MVA'])

    for bus in buses:
        if psspy.busexs(bus) == 0:
            ierr, bus_type = psspy.busint(bus, 'TYPE')
            ierr, bus_MVA = psspy.busdt1(bus, 'MVA', 'NOM')
            ierr, gen_MVA = psspy.gendt1(bus)
        if psspy.busexs(bus) == 1:
            bus_type = 0
            bus_MVA = 0
            gen_MVA = 0
        df_temp = {'Bus Number': bus, 'Type': bus_type, 'Bus MVA': bus_MVA, 'Gen MVA': gen_MVA}
        bus_df = bus_df._append(df_temp, ignore_index=True)



    return bus_df

