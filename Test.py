import os


def test():
    print("Select the case number to run")
    case = input("\n 1.Water Valley; 2.Trigo Solar; 3.BRP Bonete; 4.SMT Ironman; 5.Big Star; 6.Brotherton; 7.Pecan Praire")
    loading = input("\n Enter loading: ")

    if case == '1':
        filename = 'Water Valley'
        confolder = '22SSWG_2027_SUM1' #for now only one case and its corresponding contingencies are considered
        buses = '976014'
    elif case == '2':
        filename = 'Trigo Solar'
        confolder = '21SSWG_2025_SUM1'
        buses = '555705'
    elif case == '3':
        filename = 'BRP Bonete'
        confolder = '21SSWG_2023_SUM1'
        buses = '888000'
    elif case == '4':
        filename = 'SMT Ironman'
        confolder = '21SSWG_2025_SUM1'
        buses = '943037, 943036'
    elif case == '5':
        filename = 'Big Star'
        confolder = '20SSWG_2022_SUM1'
        buses = '100001, 100011, 100009'
    elif case == '6':
        filename = 'Brotherton'
        confolder = '22SSWG_2025_SUM1'
        buses = '996941'
    elif case == '7':
        filename = 'Pecan Praire'
        confolder = '22SSWG_2025_SUM1'
        buses = '995967, 994967'

    return filename, loading, confolder, buses

if __name__ == '__main__':
    filename, loading, confolder = test()
