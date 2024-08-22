import rasterio
import rasterio.warp
import os
import datetime
import json
import urllib.parse
from io import BytesIO
from functools import partial
from concurrent import futures
import httpx
import numpy
from boto3.session import Session as boto3_session
from rasterio.plot import reshape_as_image
from rasterio.features import bounds as featureBounds
from tqdm.notebook import tqdm
from folium import Map, TileLayer, GeoJson
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
with rasterio.open(r'C:\Users\S0KAINA ERRAMI\Downloads\imageToDriveExample_transform (10).tif') as dataset:

    # Read the dataset's valid data mask as a ndarray.
    mask = dataset.dataset_mask()

    # Extract feature shapes and values from the array.
    for geom, val in rasterio.features.shapes(
            mask, transform=dataset.transform):

        # Transform shapes from the dataset's own coordinate
        # reference system to CRS84 (EPSG:4326).
        geom = rasterio.warp.transform_geom(
            dataset.crs, 'EPSG:4326', geom, precision=6)

        # URL of the titiler endpoint
        titiler_endpoint = "https://titiler.xyz"  # Developmentseed demo endpoint. Please be kind
        # New GeoJSON with different coordinates
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": geom
    }
  ]
}

                       

        # Calculate the limits of the polygon
        bounds = featureBounds(geojson)
        # Create the map
        m = Map(
            tiles="OpenStreetMap",
            location=((bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2),
            zoom_start=10
        )
        # Add the GeoJSON to the map
        GeoJson(geojson).add_to(m)
        # Save the map as an HTML file
        m.save('map.html')
        # Open the map in the browser
        import webbrowser
        webbrowser.open('map.html')
         # Print GeoJSON shapes to stdout.
        print(geom)