from config.definitions import ROOT_DIR
import os, sys
import numpy as np
import pandas as pd
import getcounty as gc


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

    bus_df = pd.DataFrame(columns =['Bus Number', 'Type', 'Bus kV', 'Load MW', 'Gen MW'])

    for bus in buses:
        if psspy.busexs(bus) == 0:
            ierr, bus_type = psspy.busint(bus, 'TYPE')
            ierr, bus_V = psspy.busdat(bus, 'BASE')
            load_MW = 0
            gen_MW = 0
            if bus_type == 1:
                load = 0
                ierr, load = psspy.busdt2(bus, 'MVA', 'NOM')
                load_MW = load.real
                # ierr, load_count = psspy.busint(bus, 'NUMBER')
                # if load_count is not None:
                #     for load_index in range(1, load_count + 1):
                #         ierr, load_id = psspy.lodint(bus, load_index, 'NUMBER')
                #         ierr, load_MW_ind = psspy.load_data_6(bus, load_id, '', 1)
                #         load_MW += load_MW_ind
            if bus_type == 2:
                mw = 0.0
                ierr, mw = psspy.gendt1(bus)
                gen_MW = mw
                # ierr, gen_count = psspy.busint(bus, 'NUMBER')
                # if gen_count is not None:
                #     for gen_index in range(1, gen_count + 1):
                #         ierr, gen_id = psspy.macint(bus, gen_index, 'NUMBER')
                #         ierr, gen_MW_ind = psspy.macdat(bus, gen_id, 'PGENMAX')
                #         gen_MW += gen_MW_ind
        if psspy.busexs(bus) == 1:
            bus_type = 0
            load_MW = 0
            gen_MW = 0
        df_temp = {'Bus Number': bus, 'Type': bus_type, 'Bus kV': bus_V, 'Load MW': load_MW, 'Gen MW': gen_MW}
        bus_df = bus_df._append(df_temp, ignore_index=True)



    return bus_df

