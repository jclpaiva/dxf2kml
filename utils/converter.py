import ezdxf
import simplekml
import streamlit as st
from pyproj import Transformer

def get_dxf_statistics(doc):
    """Get statistics about the DXF file"""
    stats = {
        'total_entities': 0,
        'layers': set(),
        'polylines': 0
    }
    
    for entity in doc.modelspace():
        stats['total_entities'] += 1
        stats['layers'].add(entity.dxf.layer)
        if entity.dxftype() == 'LWPOLYLINE':
            stats['polylines'] += 1
            
    return {
        'total_entities': stats['total_entities'],
        'total_layers': len(stats['layers']),
        'layer_names': list(stats['layers']),
        'polylines': stats['polylines']
    }

def convert_dxf_to_kml(input_file, epsg_code):
    try:
        doc = ezdxf.readfile(input_file)
        st.info("DXF file loaded successfully.")
        
        # Get statistics before conversion
        stats = get_dxf_statistics(doc)
        
    except IOError:
        raise RuntimeError("Could not open DXF file. Please check the file path.")

    # Create a KML object
    kml = simplekml.Kml()

    # Create a transformer to convert from the specified EPSG to WGS84 (EPSG:4326)
    transformer = Transformer.from_crs(f"EPSG:{epsg_code}", "EPSG:4326", always_xy=True)

    entity_count = 0
    progress_bar = st.progress(0)
    total_entities = stats['polylines']
    
    for entity in doc.modelspace():
        if entity.dxftype() == 'LWPOLYLINE':
            # Extract vertices from the polyline and transform them to WGS84
            points = []
            for point in entity.vertices():
                x, y = point[0], point[1]
                lon, lat = transformer.transform(x, y)  # Transform coordinates
                points.append((lon, lat))  # KML expects (longitude, latitude)
            
            # Create a LineString in the KML
            line = kml.newlinestring(name=f"Polyline {entity_count + 1}", coords=points)
            line.style.linestyle.color = simplekml.Color.blue  # Blue color
            line.style.linestyle.width = 2  # Line thickness
            
            # Add structured metadata using ExtendedData
            extended_data = simplekml.ExtendedData()
            extended_data.newdata(name="Layer", value=getattr(entity.dxf, 'layer', 'Unknown'))
            extended_data.newdata(name="SubClasses", value="AcDbEntity:AcDbPolyline")
            extended_data.newdata(name="EntityHandle", value=getattr(entity.dxf, 'handle', 'Unknown'))
            line.extendeddata = extended_data
            
            entity_count += 1
            progress_bar.progress(entity_count / total_entities if total_entities > 0 else 0)

    if entity_count == 0:
        raise RuntimeError("No valid entities found in the DXF file.")

    # Return the KML content as a string
    return kml.kml(), stats