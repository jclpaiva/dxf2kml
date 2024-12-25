import streamlit as st
from utils.converter import convert_dxf_to_kml
from utils.preview import preview_kml
from utils.styles import apply_custom_styles
from utils.actions import exit_application, handle_reset
import tempfile
import os

st.set_page_config(
    page_title="DXF to KML Converter",
    layout="centered"
)

def main():
    apply_custom_styles()
    
    st.title("DXF to KML Converter")
    st.write("Convert DXF files to KML format with EPSG transformation.")
    
    # Add exit button at the top
    if st.button("Exit Application", type="secondary"):
        exit_application()
    
    # File uploader with unique key
    dxf_file = st.file_uploader(
        "Select a DXF file", 
        type=["dxf"],
        key="dxf_uploader"
    )
    
    if dxf_file is not None:
        dxf_filename = dxf_file.name
        output_file = dxf_filename[:-4] + ".kml" if dxf_filename.lower().endswith(".dxf") else dxf_filename + ".kml"
        
        epsg_options = {
            "Portugal Mainland: 3763": 3763,
            "Madeira: 32767": 32767,
            "Azores: 32768": 32768
        }
        epsg_choice = st.selectbox("Select EPSG code", list(epsg_options.keys()))
        epsg_code = epsg_options[epsg_choice]

        output_file = st.text_input("Output file name:", output_file)

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Convert", type="primary", use_container_width=True):
                if dxf_file is not None:
                    with st.spinner("Converting..."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as temp_dxf:
                            temp_dxf.write(dxf_file.read())
                            temp_dxf.close()

                        try:
                            stats = convert_dxf_to_kml(temp_dxf.name, output_file, epsg_code)
                            st.success(f"Conversion successful! File saved as {output_file}")
                            
                            # Preview KML
                            preview_kml(output_file)
                            
                        except Exception as e:
                            st.error(f"Conversion failed: {str(e)}")
                        finally:
                            os.remove(temp_dxf.name)
                else:
                    st.error("Please upload a DXF file.")
        
        with col2:
            if st.button("Reset", type="secondary", use_container_width=True):
                handle_reset()

if __name__ == "__main__":
    main()