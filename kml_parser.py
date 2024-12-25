import xml.etree.ElementTree as ET
import re
from typing import List, Tuple

def parse_coordinates(coord_str: str) -> List[Tuple[float, float]]:
    """Parse KML coordinate string into list of (lat, lon) tuples"""
    # Updated regex to extract lat/lon, ignoring altitude
    coord_pairs = re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*),?-?\d*\.?\d*?', coord_str)
    return [(float(lat), float(lon)) for lon, lat in coord_pairs]

def extract_features(kml_file: str) -> List[List[Tuple[float, float]]]:
    """Extract all coordinate features from KML file"""
    tree = ET.parse(kml_file)
    root = tree.getroot()
    
    features = []
    coords_elements = root.findall(".//{http://www.opengis.net/kml/2.2}coordinates")
    
    for coords in coords_elements:
        coord_str = coords.text.strip()
        points = parse_coordinates(coord_str)
        if points:
            features.append(points)
    
    return features