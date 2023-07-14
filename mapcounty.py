import os
from config.definitions import ROOT_DIR
import getcounty as gc
import geopandas
import matplotlib.pyplot as plt

def mapcounty(county):
    path_to_data = os.path.join(ROOT_DIR, 'Input Data\TexasCountyMap\Texas Counties Map.geojson')
    texas = geopandas.read_file(path_to_data)
    ax = texas.plot(color='white', edgecolor='black')
    ax.set_axis_off()
    plt.show()
    print(texas)

def main():
    county = gc.main()
    mapcounty(county)

if __name__ == "__main__":
    main()