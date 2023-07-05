import pyPowerGEM.wrapper as pw
import pyPowerGEM.pyTARA as pt
import os,sys,shutil
import pandas as pd
from string import Template
import numpy as np
#import config_parser_helper as cph
from config.definitions import ROOT_DIR

def read_input_files():  # Read all input files needed for performing the Flowgate screening in TARA
    cwd = os.path.join(ROOT_DIR, 'Input Data/')
    study_file = ''
    sub_file = ''
    mon_file = ''
    con_file = ''
    exc_file = ''
    files_folder = os.path.join(cwd, 'files')
    temp_folder = os.path.join(ROOT_DIR, 'Temp') #contingencies are combined and output in the Temp folder
    main_reports = os.path.join(cwd, 'main_reports')
    ind_gens = os.path.join(cwd, 'ind_gens')
    templates_folder = os.path.join(cwd, 'templates')
    for file in os.listdir(temp_folder):
        if file.endswith(".con"):
            study_file = os.path.join(files_folder, file)
    for file in os.listdir(files_folder):
        if file.endswith(".raw"):
            study_file = os.path.join(files_folder, file)
        if file.endswith(".sub"):
            sub_file = os.path.join(files_folder, file)
        if file.endswith(".mon"):
            mon_file = os.path.join(files_folder, file)
        if file.endswith(".con"):
            con_file = os.path.join(files_folder, file)
        if file.endswith(".exc"):
            exc_file = os.path.join(files_folder, file)
        if file.endswith(".csv"):
            gens_file = os.path.join(files_folder, file)
    if study_file == '' or sub_file == '' or mon_file == '' or con_file == '' or gens_file == '':
        sys.exit('ERROR MISSING SIMULATION FILE')
    if exc_file == '':
        print('NO EXCLUDE FILE LOADED')
    dfax_report_folder = os.path.join(cwd, 'screening_dfax_reports')
    create_fgt_temp = os.path.join(templates_folder, 'create_flowgate.template')
    read_sub_temp = os.path.join(templates_folder, 'read_sub.template')
    fgt_screen_temp = os.path.join(templates_folder, '1_screening.template')
    fgt_rep_temp = os.path.join(templates_folder, '2_All_fgts.template')
    ind_rep_temp = os.path.join(templates_folder, '3_ind_gen.template')
    # Flowgates created by the script will be saved in the temp folder with the following path
    fgt_file = os.path.join(temp_folder, '1_flowgates.fgt')
    run_fgt_ac = os.path.join(templates_folder, 'run_fgt.template')
    results = os.path.join(cwd, 'results')
    return {'results': results, 'files': files_folder, 'cwd': cwd, 'study': study_file, 'mon': mon_file,
            'sub': sub_file, 'con': con_file, 'gens_file': gens_file, \
            'create_fgt_temp': create_fgt_temp, 'run_fgt_ac': run_fgt_ac, 'temp': temp_folder, 'fgt_file': fgt_file,
            'read_sub_temp': read_sub_temp, \
            'fgt_screening': fgt_screen_temp, 'fgt_rep': fgt_rep_temp, 'dfax_report_folder': dfax_report_folder,
            'main_reports': main_reports, 'ind_gens': ind_gens, 'ind_rep': ind_rep_temp}


def run_tara_template(files):
    template = os.path.join(files['temp'], 'template_run')
    tara_exe = pw.powerGemExe(exeFilePath=os.path.join(os.getcwd(), "tara.exe"))
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


def run_fgt_screening(files,
                      settings):  # Perform flowgate screening using templates and the input files to get the .fgt file
    template_file = files['fgt_screening']
    config_dict = {'temp': files['temp'], 'study': files['study'], 'sub': files['sub'], 'con': files['con'],
                   'mon': files['mon'], 'max_transfer': settings['max_transfer'], \
                   'dfax': settings['dfax'], 'sending': settings['sending'], 'reference': settings['reference'],
                   'main_reports': files['main_reports'], 'load_cutoff': settings['load_cutoff']}
    mod_template(template_file, config_dict, files)
    run_tara_template(files)


def main(cris_settings, files):
    run_fgt_screening(files, cris_settings)


if __name__ == "__main__":
    files = read_input_files()
    ini_file = 'cris_settings.ini'
    init = cph.Initializer(ini_file)
    cris_settings = init.parse_ini()
    main(cris_settings['settings'], files)