import os
from config.definitions import ROOT_DIR
import getcounty as gc
import geopandas
import matplotlib.pyplot as plt

def mapcounty(county, SA_county):

    path_to_data = os.path.join(ROOT_DIR, 'Input Data\TexasCountyMap\Texas Counties Map.geojson')
    texas_map = geopandas.read_file(path_to_data)
    # Filter the Texas map to include only the selected counties
    highlighted_map = texas_map[texas_map['name'].str.lower().isin([x.lower() for x in county])]
    sacounty = texas_map[texas_map['name'].str.lower().isin([SA_county.lower()])]
    print(highlighted_map)
    print(sacounty)
    fig, ax = plt.subplots(figsize=(10, 10))
    texas_map.plot(ax=ax, color='lightgray', edgecolor='black')
    highlighted_map.plot(ax=ax, color='red', edgecolor='black')
    sacounty.plot(ax=ax, color='blue', edgecolor='black')
    highlighted_map.apply(lambda x: ax.annotate(text=x['name'], xy=x.geometry.centroid.coords[0], ha='center', fontsize=6), axis=1)
    sacounty.apply(lambda x: ax.annotate(text=SA_county, xy=x.geometry.centroid.coords[0], ha='center', fontsize=6), axis=1)
    ax.set_axis_off()
    plt.show()
    #filename = '{}{}'.format(savemap, 'Map.jpg')
    #plt.savefig(os.path.join(ROOT_DIR, 'Input Data\\SSWGCase\\', filename))
    #print(texas)

def main(filename, sacounty):
    county = gc.main(filename)
    mapcounty(county, sacounty)

# if __name__ == "__main__":
#     filename = 'BRP Bonete'
#     main(filename)