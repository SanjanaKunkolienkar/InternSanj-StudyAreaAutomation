import os
import pandas as pd
from config.definitions import ROOT_DIR

#Initially it extracts buses individually and send to get counties
#Ultimately, it should combine all buses together and then send to get counties
def extract_from_fg_violations():
    filepath = os.path.join(ROOT_DIR, 'Temp\main_reports\ViolationScreenSum.csv')
    viol = (pd.read_csv(filepath, skiprows=10)).iloc[:,0]
    buses = []
    #print(viol.head())
    for num in viol:
        words = (num.strip()).split(" ")
        word = [x for x in words if x != '']
        buses.append(int(word[0]))
        buses.append(int(word[3]))
    unique_buses = [*set(buses)]
    #print(len(buses))
    #print(len(unique_buses))
    return unique_buses

def main():
    action = 'flowgatescreening'
    if action == 'flowgatescreening':
        buses = extract_from_fg_violations()
        return buses

if __name__ == "__main__":
    action = 'flowgatescreening'
    buses = main()