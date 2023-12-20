from geopandas import gpd

gdf = gpd.read_file('./tz_world_mp.shp')

# Write GeoJSON file
gdf.to_file('./tz.geojson', driver='GeoJSON')