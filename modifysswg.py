import read_user_input as read
from config.definitions import ROOT_DIR
import os, sys
def main():
    filename, casename, loading, confolder, genbuses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level = read.main()
    cwd = os.path.join(ROOT_DIR, 'Input Data\SSWG Cases\\')
    for file in os.listdir(os.path.join(cwd)):
        if file.endswith(".sav") and file.startswith(casename):
            case_file = os.path.join(cwd, file)

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
            print("SSWG case", casename, "loaded succesfully")


if __name__ == "__main__":
    main()