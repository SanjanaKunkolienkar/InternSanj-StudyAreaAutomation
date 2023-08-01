from config.definitions import ROOT_DIR
import os, sys
import numpy as np
import pandas as pd
import mapcounty as mc
import getcounty as gc
import Test_voltage as tst

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
import redirect
redirect.psse2py()
import psspy
ierr = psspy.psseinit(150000)
psspy.lines_per_page_one_device(1, 100000)

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()

def get_n_levels_away(POI, levels):
    ibus = int(POI)
    ms = True
    flag = 2
    buses = {}
    if levels != 0:
        busdict = {ibus: 0}  # dict with level for each analysed bus
        nextbuses = [ibus]  # start search at ibus
        # For each level out into the grid
        for level in range(levels):
            searchbuses = list(nextbuses)  # buses for next level search
            nextbuses = {}  # New buses at next level - dictionary
            # For each start node at this level
            for bus in searchbuses:
                if ms:
                    ierr = psspy.inibrx(bus, 2)
                else:
                    ierr = psspy.inibrn(bus, 2)
                while ierr == 0:  # for every connection to bus
                    ierr, tbus, kbus, ickt = psspy.nxtbrn3(bus)
                    if ierr > 0: break
                    if kbus == 0:  # branch or 2W
                        ier2, st = psspy.brnint(bus, tbus, ickt, 'STATUS')
                    else:  # 3W
                        ier2, st = psspy.tr3int(bus, tbus, kbus, ickt, 'STATUS')
                    if flag == 1 or st == 1:
                        if tbus not in busdict:  # tbus at next level
                            busdict[tbus] = level + 1
                            nextbuses[tbus] = level + 1
                        if kbus > 0:
                            if kbus not in busdict:  # kbus at next level
                                busdict[kbus] = level + 1
                                nextbuses[kbus] = level + 1
            buses = buses | nextbuses
                #level = level + 1  # jbus found
    else:
        print("ERROR : Value of level is 0")

    bus_list = list(buses.keys())
    return bus_list


def main(filename, POI_bus, level, SA_county):
    cwd = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename)
    for file in os.listdir(os.path.join(cwd, 'Study Case')):
        if file.endswith(".raw"):
            study_file = os.path.join(cwd, 'Study Case', file)
    psspy.read(0, study_file)
    bus_list = get_n_levels_away(POI_bus, level)
    print("Buses N levels away")
    print(bus_list)
    county = gc.getcounty(bus_list, SA_county)
    #mc.mapcounty(county, SA_county)

    print('Buses are', bus_list)

    ierr_close_line = psspy.close_powerflow()
    ierr_del_tmpfiles = psspy.deltmpfiles()
    ierr_halt = psspy.pssehalt_2()

    return county


if __name__ == "__main__":
    level = [10, 8, 6, 4]
    buses = ['76002']
    filename = 'Brotherton'
    for bus in buses:
        print('####FOR BUS######', bus)
        for lvl in level:
            print('####FOR LEVEL######', lvl)
            county = main(filename, int(bus), lvl)