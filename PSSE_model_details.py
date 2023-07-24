from config.definitions import ROOT_DIR
import os, sys, glob

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
import psspy
import pssarrays
import epe_generic_tools as egt
import pssexcel

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()

redirect.psse2py()
ierr = psspy.psseinit(150000)
psspy.lines_per_page_one_device(1, 100000)
def bus_vals(bus):
    ierr, volt_base = psspy.busdat(bus, 'BASE')
    ierr, volt_pu = psspy.busdat(bus, 'PU')
    ierr, volt_angle = psspy.busdat(bus, 'ANGLED')

    return volt_base, volt_pu, volt_angle

def main():
    direct = os.getcwd()
    rootdir = direct
    cases = glob.glob("*.sav") + glob.glob("*.raw")





if __name__ == "__main__":
    main()