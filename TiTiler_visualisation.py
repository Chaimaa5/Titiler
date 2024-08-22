import json
import httpx
from folium import Map, TileLayer

# Define the Titiler endpoint and the COG URL
titiler_endpoint = "https://titiler.xyz"
image_url = "https://opendata.digitalglobe.com/events/mauritius-oil-spill/post-event/2020-08-12/105001001F1B5B00/105001001F1B5B00.tif"

# Function to fetch the bounds of the COG
def fetch_bounds(url):
    response = httpx.get(f"{titiler_endpoint}/cog/info", params={"url": url})
    return response.json()["bounds"]

# Function to fetch statistics of the COG
def fetch_statistics(url):
    response = httpx.get(f"{titiler_endpoint}/cog/statistics", params={"url": url})
    return response.json()

# Function to fetch TileJSON for the COG
def fetch_tilejson(url):
    response = httpx.get(f"{titiler_endpoint}/cog/WebMercatorQuad/tilejson.json", params={"url": url})
    return response.json()

# Main function to create the map
def main():
    # Fetch bounds
    bounds = fetch_bounds(image_url)
    print(f"Bounds: {bounds}")

    # Fetch statistics
    stats = fetch_statistics(image_url)
    print(json.dumps(stats, indent=4))

    # Fetch tilejson
    tilejson = fetch_tilejson(image_url)

    # Create a map
    m = Map(location=((bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2), zoom_start=13)

    # Add the tile layer to the map
    TileLayer(
        tiles=tilejson["tiles"][0],
        opacity=1,
        attr="DigitalGlobe OpenData"
    ).add_to(m)

    # Save the map to an HTML file
    m.save("cog_map.html")
    print("Map has been saved as 'cog_map.html'")
    import webbrowser
    webbrowser.open('cog_map.html')
if __name__ == "__main__":
    main()
