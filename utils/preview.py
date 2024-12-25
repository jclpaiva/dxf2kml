import streamlit as st
import folium
from streamlit_folium import folium_static
from .kml_parser import extract_features
from .map_utils import create_base_map, create_feature_group

def preview_kml(kml_file: str) -> None:
    """Display KML file on an interactive map"""
    try:
        # Extract features from KML
        features = extract_features(kml_file)
        if not features:
            st.warning("No valid features found in KML file")
            return
        
        # Create map centered on features
        m = create_base_map(features)
        
        # Add KML features
        fg = create_feature_group(features)
        fg.add_to(m)
        
        # Add layer control
        folium.LayerControl(position='topright').add_to(m)
        
        # Display map
        st.write("### KML Preview")
        folium_static(m)
        
        # Add download button
        with open(kml_file, 'rb') as f:
            st.download_button(
                label="Download KML file",
                data=f,
                file_name=kml_file,
                mime="application/vnd.google-earth.kml+xml"
            )
    
    except Exception as e:
        st.error(f"Error previewing KML: {str(e)}")