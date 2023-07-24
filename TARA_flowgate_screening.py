import pyPowerGEM.wrapper as pw
import pyPowerGEM.pyTARA as pt
import os,sys,shutil
import pandas as pd
from string import Template
import numpy as np
#import config_parser_helper as cph
from config.definitions import ROOT_DIR

def read_input_files(filename):  # Read all input files needed for performing the Flowgate screening in TARA
    cwd = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename)
    study_file = ''
    sub_file = ''
    mon_file = ''
    con_file = ''
    exc_file = ''
    files_folder = os.path.join(cwd, 'files') #contains .con , .sub , .mon  .exc and .csv files
    if not os.path.exists(os.path.join(cwd, 'Temp')):
        os.makedirs(os.path.join(cwd, 'Temp'))
    temp_folder = os.path.join(cwd, 'Temp')
    templates_folder = os.path.join(ROOT_DIR, 'Input Data\\templates\\')
    tara_folder = os.path.join(ROOT_DIR, 'Input Data\\tara\\')
    if not os.path.exists(os.path.join(temp_folder, 'main_reports')):
        os.makedirs(os.path.join(temp_folder, 'main_reports'))
    main_reports = os.path.join(temp_folder, 'main_reports')
    for file in os.listdir(os.path.join(cwd, 'Study Case')):
        if file.endswith(".raw"):
            study_file = os.path.join(cwd, 'Study Case', file)
    for file in os.listdir(files_folder):
        if file.endswith(".sub"):
            sub_file = os.path.join(files_folder, file)
        if file.endswith(".mon"):
            mon_file = os.path.join(files_folder, file)
        if file.endswith(".con"):
            con_file = os.path.join(files_folder, file)
        if file.endswith(".exc"):
            exc_file = os.path.join(files_folder, file)
    if study_file == '' or sub_file == '' or mon_file == '' or con_file == '':
        sys.exit('ERROR MISSING SIMULATION FILE')
    if exc_file == '':
        print('NO EXCLUDE FILE LOADED')
    if not os.path.exists(os.path.join(temp_folder, 'screening_dfax_reports')):
        os.makedirs(os.path.join(temp_folder, 'screening_dfax_reports'))
    else:
        for f in os.listdir(os.path.join(temp_folder, 'screening_dfax_reports')):
            os.remove(os.path.join(os.path.join(temp_folder, 'screening_dfax_reports'), f))
    dfax_report_folder = os.path.join(temp_folder, 'screening_dfax_reports')
    create_fgt_temp = os.path.join(templates_folder,'create_flowgate.template')
    read_sub_temp = os.path.join(templates_folder,'read_sub.template')
    fgt_screen_temp = os.path.join(templates_folder, '1_screening.template')
    fgt_rep = os.path.join(templates_folder, '2_All_fgts.template')
    # Flowgates created by the script will be saved in the temp folder with the following path
    fgt_file = os.path.join(temp_folder, '1_flowgates.fgt')
    run_fgt_ac = os.path.join(templates_folder, 'run_fgt.template')
    results = os.path.join(temp_folder, 'results')

    print("Read input files for TARA flowgate screening in ", filename)
    return {'results': results, 'files': files_folder, 'cwd': cwd, 'study': study_file, 'mon': mon_file,
            'sub': sub_file, 'con': con_file, 'run_fgt_ac': run_fgt_ac, 'temp': temp_folder, 'fgt_file': fgt_file,
            'fgt_screening': fgt_screen_temp, 'dfax_report_folder': dfax_report_folder,'main_reports': main_reports,
            'tara': tara_folder, 'fgt_rep': fgt_rep, 'create_fgt_temp':create_fgt_temp, 'read_sub_temp':read_sub_temp,}

def run_tara_template(files):
    template = os.path.join(files["temp"], 'template_run')
    tara_exe = pw.powerGemExe(exeFilePath=os.path.join(files['tara'], 'tara.exe'))
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

def run_fgt_screening(files, loading, dfax_cutoff):# Perform flowgate screening using templates and the input files to get the .fgt file
    template_file = files['fgt_screening'] #fgt_screen_temp file path = 1_screening.template
    config_dict = {'temp': files['temp'], 'study': files['study'], 'sub': files['sub'], 'con': files['con'],
                   'mon': files['mon'], 'main_reports': files['main_reports'], 'loading': loading, 'dfax': dfax_cutoff}
    mod_template(template_file, config_dict, files)
    run_tara_template(files)

def run_fgt_report(files, loading, dfax_cutoff):
    viol_screen_sum = os.path.join(files['main_reports'], 'ViolationScreenSum.csv')  # reads the flowgate screening results
    df = pd.read_csv(viol_screen_sum, skiprows=10, header=0)  # skips to the results to count the number of flowgates
    print(df)
    df = df.rename(columns=lambda x: x.strip())
    value = loading
    df = df.rename(columns={"Loading%": "Loading"})
    df[['Loading']] = df[['Loading']].astype(int)
    df = df[df.Loading >= value]
    df.to_csv(os.path.join(files['main_reports'], 'ViolationScreenSum_loading.csv'))
    dfax_report_txt = 'opt report\n\
      MWCutOff        2 //MW impact cutoff for detatiled report\n\
      LimitCutOff     1 //Detailed report cutoff based on % of rating\n\
      maxGenDetReport 20 //Max number of generators on detailed report\n\
      SortDetailedRep 2 //Sorting detailed report\n\
      SensCutOffLoad  $dfax //Detailed report load distribut. factors cutoff [0-1]\n\
      MWCutOffLoad    0 //MW impact load cutoff for detailed report\n\
      SensCutOff      $dfax //Generator Distribut. factors cutoff\n\
    0 0\n\
    opt analys\n\
      wdSubSysName    Export\n\
      wdSubSysRefName Import\n\
    0 0\n\
    Detailed %save "$dfax_report_folder\$fgt_num.csv" %csv Dfax $fgt_num 0\n\
    chdir "$temp"'
    dfax_report_template = Template(dfax_report_txt)
    all_fgt_rep = ''
    for fgt_num in list(range(1, len(df.index) + 1)):
        config_dict = {'temp': files['temp'], 'dfax_report_folder': files['dfax_report_folder'],
                       'fgt_num': fgt_num, 'dfax': dfax_cutoff}
        sub_txt = dfax_report_template.substitute(**config_dict)
        if all_fgt_rep == '':
            all_fgt_rep = sub_txt
        else:
            all_fgt_rep += '\n'
            all_fgt_rep += sub_txt
    template_file = files['fgt_rep']
    config_dict = {'temp': files['temp'], 'study': files['study'], 'sub': files['sub'], 'all_fgt_rep': all_fgt_rep,
                   'fgt_file': files['fgt_file'], 'main_reports': files['main_reports'], 'dfax': dfax_cutoff}
    mod_template(template_file, config_dict, files)
    run_tara_template(files)

# merge the dfax reports into one single table to include all study gens, and identifying the flowgate id in the header, find CRIS values after dispatching all units to 100%
def create_har_ref(files, dfax_cutoff):
    all_csv_files = []
    for file in os.listdir(files['dfax_report_folder']):
        if file.endswith(".csv"):
            all_csv_files.append(os.path.join(files['dfax_report_folder'], file))

    filtered_mon = pd.DataFrame(columns=['Fgt Name', 'Cont Name', 'Max Dfax'])
    fgt_name = []
    cont_name= []
    max_dfax = []
    for file in all_csv_files:
        fgt_idx = int(file.split("\\")[-1].split(".")[0])
        df_dfax = pd.read_csv(file, skiprows=15)
        df_dfax = df_dfax.rename(columns=lambda x: x.strip())
        df_fgt_name = pd.read_csv(file, skiprows=lambda x: x not in [9, 10, 11])
        df_fgt_name = df_fgt_name.rename(columns=lambda x: x.strip())
        mon = df_fgt_name.iloc[0, 0].split("=", 1)[1].strip()
        con = df_fgt_name.iloc[1, 0].split("=", 1)[1].strip()
        df_dfax.drop(df_dfax.columns[[-1, ]], axis=1, inplace=True)
        if ((df_dfax['Dfax'].astype(float)).max()>dfax_cutoff or ((df_dfax['Dfax'].astype(float)).min()<(-1*dfax_cutoff))):
            fgt_name.append(mon)
            cont_name.append(con)
            max_dfax.append(df_dfax['Dfax'].max())

    filtered_mon['Fgt Name'] = fgt_name
    filtered_mon['Cont Name'] = cont_name
    filtered_mon['Max Dfax'] = max_dfax
    filtered_mon.to_csv(os.path.join(files['temp'], 'FilteredFlowgates.csv'))

def main(files, loading, dfax_cutoff):
    run_fgt_screening(files, loading, dfax_cutoff)
    run_fgt_report(files, loading, dfax_cutoff)
    create_har_ref(files, dfax_cutoff)
    print("Generated Flowgate Screening files")

# if __name__ == "__main__":
#     filename = 'Pecan Praire'
#     loading = 40
#     files = read_input_files(filename) #read .mon , .con , .sub , .raw files
#     main(files, loading)