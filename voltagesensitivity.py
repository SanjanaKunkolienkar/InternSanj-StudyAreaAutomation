from config.definitions import ROOT_DIR
import os, sys
import numpy as np
import pandas as pd
import getcounty as gc

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
def bus_vals(bus):
    ierr, volt_base = psspy.busdat(bus, 'BASE')
    ierr, volt_pu = psspy.busdat(bus, 'PU')
    ierr, volt_angle = psspy.busdat(bus, 'ANGLED')

    return volt_base, volt_pu, volt_angle

def read_input(filename):
    cwd = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename)
    for file in os.listdir(os.path.join(cwd, 'Study Case')):
        if file.endswith(".raw"):
            study_file = os.path.join(cwd, 'Study Case', file)
    for file in os.listdir(os.path.join(cwd, 'Bench Case')):
        if file.endswith(".raw"):
            bench_file = os.path.join(cwd, 'Bench Case', file)

    return {'study': study_file, 'bench': bench_file}

def get_voltage():
    _, (voltages,) = psspy.abusreal(string='PU')
    _, (buses,) = psspy.abusint(string='NUMBER')
    voltages = np.array(voltages)
    buses = np.array(buses)

    return voltages, buses

def read_psse_output_voltage(filename, studypath, benchpath):

    psse_files = read_input(filename)
    redirect.psse2py()
    psspy.psseinit(150000)
    psspy.read(0, psse_files['study'])
    study_V, study_B = get_voltage()

    study_system = pd.DataFrame({'Bus Number_study': study_B, 'Voltage_study': study_V})
    study_system.to_csv(studypath)
    ierr_close_line = psspy.close_powerflow()
    ierr_del_tmpfiles = psspy.deltmpfiles()
    ierr_halt = psspy.pssehalt_2()
    psspy.stop_2()

    redirect.psse2py()
    ierr = psspy.psseinit(150000)
    psspy.lines_per_page_one_device(1, 100000)
    psspy.read(0, psse_files['bench'])
    bench_V, bench_B = get_voltage()
    bench_system = pd.DataFrame({'Bus Number_bench': bench_B, 'Voltage_bench': bench_V})
    bench_system.to_csv(benchpath)


    return studypath, benchpath

def combine_csv(filename, studypath, benchpath):
    study = pd.read_csv(studypath, usecols=["Bus Number_study", "Voltage_study"])
    bench = pd.read_csv(benchpath, usecols=["Bus Number_bench", "Voltage_bench"])

    study.set_index('Bus Number_study', inplace=True)
    bench.set_index('Bus Number_bench', inplace=True)

    combine = pd.merge(study, bench, left_index=True, right_index=True)
    combine['Sensitivity'] = 100*(combine['Voltage_bench']-combine['Voltage_study'])/combine['Voltage_bench']
    combine.to_csv(os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Voltages\Combine.csv'))

    return combine


def main(filename,voltage_cutoff, SA_county):
    filepath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Voltages')
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    studypath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Voltages\Study.csv')
    benchpath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename, 'Voltages\Bench.csv')
    read_psse_output_voltage(filename, studypath, benchpath)
    combine = combine_csv(filename,studypath, benchpath)
    #filter combine dataframe for greater than 0.05%
    filtered_combine = combine[combine['Sensitivity'].abs() > voltage_cutoff]
    #get the list of buses with voltage sensitivity > 0.05
    buses = filtered_combine.index.tolist()
    county = gc.getcounty(buses, SA_county)

    return county


if __name__ == "__main__":
    filename = 'Brotherton'
    sacounty = 'Anderson'
    voltage_cutoff = 0.05
    county = main(filename, voltage_cutoff, SA_county)
