import ezdxf
from osgeo import ogr, osr
import streamlit as st

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

def convert_dxf_to_kml(input_file, output_file, epsg_code):
    try:
        doc = ezdxf.readfile(input_file)
        st.info("DXF file loaded successfully.")
        
        # Get statistics before conversion
        stats = get_dxf_statistics(doc)
        
    except IOError:
        raise RuntimeError("Could not open DXF file. Please check the file path.")

    driver_kml = ogr.GetDriverByName('KML')
    if driver_kml is None:
        raise RuntimeError("KML driver is not available.")

    # Set KML creation options for black lines
    options = ['LINESTYLE_COLOR=ff000000']  # RGBA: Black color
    kml_ds = driver_kml.CreateDataSource(output_file, options=options)
    if kml_ds is None:
        raise RuntimeError("Failed to create KML data source.")

    srs = osr.SpatialReference()
    if srs.ImportFromEPSG(epsg_code) != 0:
        raise RuntimeError("Failed to import EPSG code.")

    kml_layer = kml_ds.CreateLayer('DXF_Layer', srs, geom_type=ogr.wkbLineString)
    if kml_layer is None:
        raise RuntimeError("Failed to create KML layer.")

    fields = {
        'Layer': ogr.OFTString,
        'SubClasses': ogr.OFTString,
        'EntityHandle': ogr.OFTString
    }
    
    for field_name, field_type in fields.items():
        field = ogr.FieldDefn(field_name, field_type)
        kml_layer.CreateField(field)

    entity_count = 0
    progress_bar = st.progress(0)
    total_entities = stats['polylines']
    
    for entity in doc.modelspace():
        if entity.dxftype() == 'LWPOLYLINE':
            line = ogr.Geometry(ogr.wkbLineString)
            for point in entity.vertices():
                line.AddPoint(point[0], point[1])

            feature = ogr.Feature(kml_layer.GetLayerDefn())
            feature.SetGeometry(line)
            
            feature.SetField('Layer', getattr(entity.dxf, 'layer', 'Unknown'))
            feature.SetField('SubClasses', 'AcDbEntity:AcDbPolyline')
            feature.SetField('EntityHandle', getattr(entity.dxf, 'handle', 'Unknown'))

            kml_layer.CreateFeature(feature)
            
            entity_count += 1
            progress_bar.progress(entity_count / total_entities if total_entities > 0 else 0)

    kml_ds = None

    if entity_count == 0:
        raise RuntimeError("No valid entities found in the DXF file.")

    return stats