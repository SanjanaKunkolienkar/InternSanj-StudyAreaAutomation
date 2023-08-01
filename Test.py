import os


def test():
    print("Select the case number to run")
    case = input("\n 1.Water Valley; 2.Trigo Solar; 3.BRP Bonete; 4.SMT Ironman; 5.Big Star; 6.Brotherton; 7.Pecan Praire")
    loading = 100 #input("\n Enter loading: ")
    dfax_cutoff = 0.03
    voltage_cutoff = 0.05
    level = int(4)

    if case == '1':
        filename = 'Water Valley'
        confolder = '22SSWG_2027_SUM1' #for now only one case and its corresponding contingencies are considered
        buses = '976014'
        SA_county = 'Tom Green'
        POI_bus = '976009'
    elif case == '2':
        filename = 'Trigo Solar'
        confolder = '21SSWG_2025_SUM1'
        buses = '555705'
        SA_county = 'McMullen'
        POI_bus = '5705'
    elif case == '3':
        filename = 'BRP Bonete'
        confolder = '21SSWG_2023_SUM1'
        buses = '888000'
        SA_county = 'Hidalgo'
        POI_bus = '8951'
    elif case == '4':
        filename = 'SMT Ironman'
        confolder = '21SSWG_2025_SUM1'
        buses = '943037, 943036'
        SA_county = 'Brazoria'
        POI_bus = '43035'
    elif case == '5':
        filename = 'Big Star'
        confolder = '20SSWG_2022_SUM1'
        buses = '100001, 100011, 100009'
        SA_county = 'Bastrop'
        POI_bus = '9043'
    elif case == '6':
        filename = 'Brotherton'
        confolder = '22SSWG_2025_SUM1'
        buses = '996941'
        SA_county = 'Anderson'
        POI_bus = '6937'
    elif case == '7':
        filename = 'Pecan Praire'
        confolder = '22SSWG_2025_SUM1'
        buses = '995967, 994967'
        SA_county = 'Leon'
        POI_bus = '999967'

    return filename, loading, confolder, buses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level

if __name__ == '__main__':
    filename, loading, confolder, SA_county, dfax_cutoff, POI_bus, level = test()
