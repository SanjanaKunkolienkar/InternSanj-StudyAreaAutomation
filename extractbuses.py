import os
import pandas as pd
from config.definitions import ROOT_DIR

#Initially it extracts buses individually and send to get counties
#Ultimately, it should combine all buses together and then send to get counties
def extract_from_fg_violations(filename):

    filepath = os.path.join(ROOT_DIR, 'Input Data\SSWGCase\\', filename , 'Temp\FilteredFlowgates.csv')
    viol = (pd.read_csv(filepath, skiprows=10)).iloc[:,1]
    buses = []
    print(viol.head())
    for num in viol:
        words = (num.strip()).split(" ")
        #print(words)
        filtered = filter(lambda x: (len(x) > 0) and (len(x) < 7), words)
        filtered_list = list(filtered)
        #print(filtered_list[0])
        word = [x for x in filtered_list if ((x == '-') or (x.isdigit())) and ((x != '138') and (x != '345') and (x != '1'))]
        #print(word)
        buses.append(int(word[0]))
        buses.append(int(word[1]))

    unique_buses = [*set(buses)]
    #print(len(buses))
    print(unique_buses)
    return unique_buses

def main(filename):
    action = 'flowgatescreening'
    if action == 'flowgatescreening':
        buses = extract_from_fg_violations(filename)
        return buses

# if __name__ == "__main__":
    #action = 'flowgatescreening'
    #filename = 'Brotherton'
    #buses = main(filename)