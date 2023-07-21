import os
from config.definitions import ROOT_DIR
import getcounty as gc
import geopandas
import matplotlib.pyplot as plt

def mapcounty(county):
    path_to_data = os.path.join(ROOT_DIR, 'Input Data\TexasCountyMap\Texas Counties Map.geojson')
    texas_map = geopandas.read_file(path_to_data)
    # Filter the Texas map to include only the selected counties
    highlighted_map = texas_map[texas_map['name'].str.lower().isin([x.lower() for x in county])]
    print(highlighted_map)
    fig, ax = plt.subplots(figsize=(10, 10))
    texas_map.plot(ax=ax, color='lightgray', edgecolor='black')
    highlighted_map.plot(ax=ax, color='red', edgecolor='black')
    highlighted_map.apply(lambda x: ax.annotate(text=x['name'], xy=x.geometry.centroid.coords[0], ha='center', fontsize=6), axis=1)
    ax.set_axis_off()
    plt.show()
    #filename = '{}{}'.format(savemap, 'Map.jpg')
    #plt.savefig(os.path.join(ROOT_DIR, 'Input Data\\SSWGCase\\', filename))
    #print(texas)

def main(filename):
    county = gc.main(filename)
    mapcounty(county)

if __name__ == "__main__":
    filename = 'Pecan Praire'
    main(filename)