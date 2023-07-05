# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
from config.definitions import ROOT_DIR

def print_folderstructure_test():
    # Use a breakpoint in the code line below to debug your script.
    print('*******This is a test to check if the code is in correct folder*******')
    print(__file__)
    print('Input folder path:', os.path.join(ROOT_DIR, 'Input Data'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_folderstructure_test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/