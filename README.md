# StudyAreaAutomation
Before running the main.py ensure the following:
1. This tool was developed with following software and version:
   1. PSSE 35.3
   2. Python 3.9
   3. TARA ??
2. All packages are installed on your computer.
3. Add the ERCOT contingencies in the Input Data/ERCOTcontingencies folder. When doing this add only the .con files corresponding to the study SSWG case.
4. Load the input files in following folders:
   1. ERCOTcontingencies: All ERCOT contingences for PSSE for the study case as .con files.
   2. files: Keep empty. The code will add .mon, .con, .sub files here.
   3. PlanningDataDictionary: ERCOT planning data dictionary
   4. SSWGCase: .raw file of the study case.