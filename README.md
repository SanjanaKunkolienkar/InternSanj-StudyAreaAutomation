# StudyAreaAutomation
Before running the main.py ensure the following:
1. This tool was developed with following software and version:
   1. PSSE 35.3
   2. Python 3.9
   3. TARA 2301_2
2. All packages are installed on your computer. Packages can be found in requirements.txt file.
3. Add the ERCOT contingencies in the Input Data/ERCOTcontingencies folder. Ensure that the contingency folder corresponding to the study SSWG case is available in this path.
4. When downloading from Github, make sure the following files are added in the respective folders:
   1. ERCOTcontingencies : Contingency folder corresponding to the SSWG case.
   2. GTClist : Can be empty.
   3. Missing Gen Files: Can be empty.
   4. Planning Data Dictionary: Has the latest ERCOT planning data dictionary modified by EPE.
   5. SSWG Cases : Input the corresponding year SSWG case.
      1. Load the input files in following folders:
         1. PlanningDataDictionary: 
         2. SSWGCase: .raw/.sav file of the study case.
         3. 