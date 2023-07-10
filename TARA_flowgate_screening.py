import pyPowerGEM.wrapper as pw
import pyPowerGEM.pyTARA as pt
import os,sys,shutil
import pandas as pd
from string import Template
import numpy as np
#import config_parser_helper as cph
from config.definitions import ROOT_DIR

def read_input_files():  # Read all input files needed for performing the Flowgate screening in TARA
    cwd = os.path.join(ROOT_DIR, 'Input Data\\')
    study_file = ''
    sub_file = ''
    mon_file = ''
    con_file = ''
    exc_file = ''
    files_folder = os.path.join(cwd, 'files') #contains .con , .sub , .mon  .exc and .csv files
    case_folder = os.path.join(cwd, 'SSWGCase') #contains the .raw file
    temp_folder = os.path.join(ROOT_DIR, 'Temp')
    templates_folder = os.path.join(temp_folder, 'templates')
    main_reports = os.path.join(temp_folder, 'main_reports')
    #ind_gens = os.path.join(cwd, 'ind_gens')
    for file in os.listdir(case_folder):
        if file.endswith(".raw"):
            study_file = os.path.join(case_folder, file)
    for file in os.listdir(files_folder):
        if file.endswith(".sub"):
            sub_file = os.path.join(files_folder, file)
        if file.endswith(".mon"):
            mon_file = os.path.join(files_folder, file)
        if file.endswith(".con"):
            con_file = os.path.join(files_folder, file) #contingencies are combined and output in the Temp folder
        if file.endswith(".exc"):
            exc_file = os.path.join(files_folder, file)
        #if file.endswith(".csv"):
        #    gens_file = os.path.join(files_folder, file)
    if study_file == '' or sub_file == '' or mon_file == '' or con_file == '':# or gens_file == '':
        sys.exit('ERROR MISSING SIMULATION FILE')
    if exc_file == '':
        print('NO EXCLUDE FILE LOADED')
    dfax_report_folder = os.path.join(temp_folder, 'screening_dfax_reports')
    create_fgt_temp = os.path.join(templates_folder, 'create_flowgate.template')
    read_sub_temp = os.path.join(templates_folder, 'read_sub.template')
    fgt_screen_temp = os.path.join(templates_folder, '1_screening.template')
    # Flowgates created by the script will be saved in the temp folder with the following path
    fgt_file = os.path.join(temp_folder, '1_flowgates.fgt')
    run_fgt_ac = os.path.join(templates_folder, 'run_fgt.template')
    results = os.path.join(temp_folder, 'results')
    return {'results': results, 'files': files_folder, 'cwd': cwd, 'study': study_file, 'mon': mon_file,
            'sub': sub_file, 'con': con_file, 'create_fgt_temp': create_fgt_temp,
            'run_fgt_ac': run_fgt_ac, 'temp': temp_folder, 'fgt_file': fgt_file, 'read_sub_temp': read_sub_temp,
            'fgt_screening': fgt_screen_temp, 'dfax_report_folder': dfax_report_folder,
            'main_reports': main_reports} #'gens_file': gens_file

def run_tara_template(files):
    template = os.path.join(files['temp'], 'template_run')
    tara_exe = pw.powerGemExe(exeFilePath="P:/TARA/New Release/TARA2102_3/tara.exe")
    print('Simulation Started')
    output = tara_exe.runScript(scriptFilePath=template)
    print(output)
    print('Simulation Finished')

def mod_template(template_file, config_dict, files):
    output_file = open(os.path.join(files['temp'], 'template_run'), "w")
    template = open(template_file, 'r')  # constructed template file with $template arguments to be swapped out
    template_read = template.read()
    template_script = Template(template_read)
    new_script = template_script.substitute(**config_dict)
    output_file.write(new_script)

def run_fgt_screening(files):  # Perform flowgate screening using templates and the input files to get the .fgt file
    template_file = files['fgt_screening'] #fgt_screen_temp file path = 1_screening.template
    config_dict = {'temp': files['temp'], 'study': files['study'], 'sub': files['sub'], 'con': files['con'],
                   'mon': files['mon'],'main_reports': files['main_reports']}
    mod_template(template_file, config_dict, files)
    run_tara_template(files)

def main(files):
    run_fgt_screening(files)

if __name__ == "__main__":
    files = read_input_files() #read .mon , .con , .sub , .raw files
    main(files)