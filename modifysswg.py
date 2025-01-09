import read_user_input as read
from config.definitions import ROOT_DIR
import os, sys
def main():
    filename, casename, loading, confolder, buses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level, number_of_gens, \
        option, gen_MW, gen_MVAR, from_bus, to_bus, percent_from_frombus = read.main()
    cwd = os.path.join(ROOT_DIR, 'Input Data\Generic SSWG Cases\\')

    for file in os.listdir(os.path.join(cwd)):
        if file.endswith(".sav") and file.startswith(casename):
            case_file = os.path.join(cwd, file)
            old_casename = '{}{}'.format(file[0:-4], '.raw')
            new_casename = '{}{}'.format(file[0:-4], '_withSA.raw')
            new_savefile = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Study Case', new_casename)
            old_savefile = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Bench Case', old_casename)
            print(old_savefile)

    ### Create folders in the directory
    if not os.path.exists(os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename)):
        os.makedirs(os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename))
    if not os.path.exists(os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Bench Case\\')):
        os.makedirs(os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Bench Case\\'))
    if not os.path.exists(os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Study Case\\')):
        os.makedirs(os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Study Case\\'))

    ## Read IDV files
    idv_files = []
    for file in os.listdir(os.path.join(cwd,'idv')):
        if file.endswith(".idv"):
            idv_files.append(file)


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


    if case_file.endswith(".sav"):
        ierr = psspy.case(case_file)
        if ierr == 0:
            print("SSWG case", casename, "loaded successfully")

    ierr = psspy.rawd_2(0,1,[1,1,1,0,0,0,2],0,old_savefile)
    print("#######RAW FILE SAVED OLD#######", ierr)
    POI_bus = int(POI_bus)
    ierr, bus_V = psspy.busdat(POI_bus, 'PU')
    ierr, bus_A = psspy.busdat(POI_bus, 'ANGLE')
    if int(option) == 1:
        psspy.bus_data_4(10, 0, [2, 1, 1, 1], [0.0, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9], "")
        psspy.bus_chng_4(10, 0, [_i, _i, _i, _i], [_f, bus_V, bus_A, _f, _f, _f, _f], _s)
        psspy.bus_number(10, 996937)
        psspy.branch_data_3(6937, 996937, r"""1""", [1, 6937, 455, 0, 0, 0],
                            [0.0, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "")
        psspy.plant_data_4(996937, 0, [0, 0], [1.0, 100.0])
        ierr = psspy.machine_data_4(996937, r"""1""", [1, 0, 0, 0, 0, 0, 0],
                             [0.0, 0.0, gen_MVAR, (-1*gen_MVAR), gen_MW, (-1*gen_MW), 100.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                              1.0, 1.0], "")
        for idvf in idv_files:
            psspy.runrspnsfile(os.path.join(os.getcwd(), idvf))
        # Run load flow
        ierr = psspy.fnsl([1, 0, 1, 1, 1, 0, 0, 0])
        print("#######POWER FLOW SOLUTION#########", ierr)
        ierr = psspy.rawd_2(sid=0,all=1,status=[1,1,1,0,0,0,1],out=0,ofile=new_savefile)
        print("#######RAW FILE SAVED NEW#######", new_savefile)
    elif int(option) == 2:
        pass
        # psspy.ltap(6935, 6937, r"""1""", 0.27, 996937, "", 138.0)
        # psspy.plant_data_4(996937, 0, [0, 0], [1.0, 100.0])
        # psspy.machine_data_4(996937, r"""1""", [1, 455, 0, 0, 0, 0, 0],
        #                      [0.0, 0.0, 9999.0, -9999.0, 9999.0, -9999.0, 100.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
        #                       1.0, 1.0], "")

    buses = '996937'
    return filename, casename, loading, confolder, buses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level, number_of_gens, \
        option, gen_MW, gen_MVAR, from_bus, to_bus, percent_from_frombus


if __name__ == "__main__":
    main()