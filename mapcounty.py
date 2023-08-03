import os
from config.definitions import ROOT_DIR
import getcounty as gc
import nlevels as nl
import geopandas
import Test as tst

import json
import random
import matplotlib.pyplot as plt
from shapely.geometry import shape, Polygon, MultiPolygon


def read_geojson():
    file_path = os.path.join(ROOT_DIR, 'Input Data\TexasCountyMap\Texas Counties Map.geojson')
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
def extract_polygons(geojson_data):
    polygons = []
    for feature in geojson_data['features']:
        geometry = shape(feature['geometry'])
        if 'name' in feature['properties']:
            name = feature['properties']['name']
        else:
            name = 'Unnamed Polygon'
        if isinstance(geometry, Polygon):
            polygons.append((geometry, name))
        elif isinstance(geometry, MultiPolygon):
            for sub_polygon in geometry.geoms:
                polygons.append((sub_polygon, name))
    return polygons


def extract_polygons_by_name(geojson_data, target_polygon_names):
    selected_polygons = []
    for feature in geojson_data['features']:
        geometry = shape(feature['geometry'])
        name = feature['properties'].get('name', None)  # Assuming the name property is present in the GeoJSON

        if isinstance(geometry, Polygon) and name and name.lower() in target_polygon_names:
            selected_polygons.append(geometry)
        elif isinstance(geometry, MultiPolygon):
            if name and name.lower() in target_polygon_names:
                selected_polygons.extend(list(geometry.geoms))

    return selected_polygons


def calculate_convex_hull(polygons):
    return MultiPolygon(polygons).convex_hull


def plot_polygons(all_polygons, selected_polygons, SA_county, county_flip):
    plt.figure(figsize=(8, 6))
    combined_county = []
    for polygon_data in all_polygons:
        if isinstance(polygon_data, tuple):
            polygon, name = polygon_data
        x, y = polygon.exterior.xy
        centroid_x, centroid_y = polygon.centroid.xy
        if polygon in selected_polygons:
            if name not in [SA_county]:
                plt.plot(x, y, 'black', linewidth=2, label='Random Polygon', fillstyle='full')
                plt.fill(x, y, 'r', alpha=0.8)
                plt.annotate(name, xy=(centroid_x[0], centroid_y[0]),
                             xytext=(centroid_x[0], centroid_y[0]),
                             fontsize=8, ha='center', va='bottom', color='black')
                combined_county.append(name)
            elif name in [SA_county]:
                plt.plot(x, y, 'black', linewidth=1)
                plt.fill(x, y, 'b', alpha=0.8)
                plt.annotate(SA_county, xy=(centroid_x[0], centroid_y[0]),
                             xytext=(centroid_x[0], centroid_y[0]),
                             fontsize=8, ha='center', va='bottom', color='black')
                combined_county.append(name)
        elif polygon.intersects(calculate_convex_hull(selected_polygons)):
            if ((polygon.intersection(calculate_convex_hull(selected_polygons)).area)*100 > 5.0) and len(county_flip) == 0:
                # print("For county", name)
                # print("Area of intersection is", polygon.intersection(calculate_convex_hull(selected_polygons)).area)
                plt.plot(x, y, 'black', linewidth=1)
                plt.fill(x, y, 'g', alpha=0.6)
                plt.annotate(name, xy=(centroid_x[0], centroid_y[0]),
                             xytext=(centroid_x[0], centroid_y[0]),
                             fontsize=8, ha='center', va='bottom', color='black')
                combined_county.append(name)
            elif ((polygon.intersection(calculate_convex_hull(selected_polygons)).area)*100 > 5.0) and len(county_flip) != 0:
                if name.lower() in county_flip:
                    plt.plot(x, y, 'black', linewidth=2, label='Random Polygon', fillstyle='full')
                    plt.fill(x, y, 'c', alpha=0.6)
                    plt.annotate(name, xy=(centroid_x[0], centroid_y[0]),
                                 xytext=(centroid_x[0], centroid_y[0]),
                                 fontsize=8, ha='center', va='bottom', color='black')
                    combined_county.append(name)
                else:
                    plt.plot(x, y, 'black', linewidth=2, label='Random Polygon', fillstyle='full')
                    plt.fill(x, y, 'g', alpha=0.8)
                    plt.annotate(name, xy=(centroid_x[0], centroid_y[0]),
                                 xytext=(centroid_x[0], centroid_y[0]),
                                 fontsize=8, ha='center', va='bottom', color='black')
                    combined_county.append(name)
        else:
            plt.plot(x, y, 'black', linewidth=1)

    convex_hull = calculate_convex_hull(selected_polygons)
    x_hull, y_hull = convex_hull.exterior.xy

    plt.plot(x_hull, y_hull, 'g-', linewidth=2, label='Convex Hull')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Counties and Convex Hull')
    plt.grid(True)
    plt.show()

    return x_hull, y_hull, combined_county

def map_study_area(county, county_flip, SA_county):
    geojson_data = read_geojson()
    all_polygons = extract_polygons(geojson_data)
    selected_polygons = extract_polygons_by_name(geojson_data, county)

    _, _, _ = plot_polygons(all_polygons, selected_polygons, SA_county, county_flip)



def main(target_polygon_names,SA_county):
    geojson_data = read_geojson()
    all_polygons = extract_polygons(geojson_data)
    selected_polygons = extract_polygons_by_name(geojson_data, target_polygon_names)

    _, _, combined_county = plot_polygons(all_polygons, selected_polygons, SA_county, [])

    return combined_county

if __name__ == "__main__":
    filename, loading, confolder, buses, SA_county, dfax_cutoff, voltage_cutoff, POI_bus, level = tst.test()
    target_polygon_names = nl.main(filename, POI_bus, level, SA_county)
    combined_county = main(target_polygon_names, SA_county)