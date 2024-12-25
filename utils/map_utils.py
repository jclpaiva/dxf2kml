import folium
from typing import List, Tuple

def calculate_zoom_level(bounds) -> int:
    """Calculate appropriate zoom level based on feature bounds"""
    lat_diff = bounds['max_lat'] - bounds['min_lat']
    lon_diff = bounds['max_lon'] - bounds['min_lon']
    
    # Use the larger difference to determine zoom
    max_diff = max(lat_diff, lon_diff)
    
    # Zoom level calculation (approximate)
    if max_diff > 5: return 8
    elif max_diff > 2: return 9
    elif max_diff > 1: return 10
    elif max_diff > 0.5: return 11
    elif max_diff > 0.1: return 12
    elif max_diff > 0.05: return 13
    elif max_diff > 0.01: return 14
    else: return 15

def get_bounds(features: List[List[Tuple[float, float]]]) -> dict:
    """Calculate bounds from all features"""
    all_lats = []
    all_lons = []
    for feature in features:
        lats, lons = zip(*feature)
        all_lats.extend(lats)
        all_lons.extend(lons)
    
    return {
        'min_lat': min(all_lats),
        'max_lat': max(all_lats),
        'min_lon': min(all_lons),
        'max_lon': max(all_lons),
        'center_lat': sum(all_lats) / len(all_lats),
        'center_lon': sum(all_lons) / len(all_lons)
    }

def create_base_map(features: List[List[Tuple[float, float]]]) -> folium.Map:
    """Create a base map centered on the features"""
    bounds = get_bounds(features)
    zoom_level = calculate_zoom_level(bounds)
    
    # Create map
    m = folium.Map(
        location=[bounds['center_lat'], bounds['center_lon']],
        zoom_start=zoom_level,
        control_scale=True
    )
    
    # Fit bounds to ensure all features are visible
    m.fit_bounds([
        [bounds['min_lat'], bounds['min_lon']],
        [bounds['max_lat'], bounds['max_lon']]
    ])
    
    add_map_layers(m)
    return m

def create_feature_group(features: List[List[Tuple[float, float]]]) -> folium.FeatureGroup:
    """Create a feature group with all KML features"""
    fg = folium.FeatureGroup(name="KML Features")
    
    for points in features:
        # Create polyline for each feature
        folium.PolyLine(
            points,
            weight=2,
            color='black',
            opacity=0.8
        ).add_to(fg)
    
    return fg

def add_map_layers(map_obj: folium.Map) -> None:
    """Add different map layers with satellite as default"""
    # Base street map layer
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Streets',
        control=True,
    ).add_to(map_obj)

    # Satellite layer (set as default)
    satellite = folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Satellite',
        overlay=True,
        control=True,
        max_zoom=22
    )
    satellite.add_to(map_obj)

    # Hybrid layer
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Hybrid',
        overlay=False,
        control=True,
        max_zoom=22
    ).add_to(map_obj)

    # Terrain layer
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr='Google',
        name='Terrain',
        overlay=False,
        control=True,
        max_zoom=22
    ).add_to(map_obj)

    # Set satellite as default
    map_obj.add_child(satellite)