import pandas as pd
import os

def get_epsg_options():
    """Read the EPSG codes from the CSV file and return a dictionary of options."""
    # Path to the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), "data", "codes.csv")
    
    # Read the CSV file with the correct encoding (ISO-8859-1)
    df = pd.read_csv(csv_path, sep=";", encoding="ISO-8859-1")
    
    # Create a dictionary of EPSG options
    epsg_options = {}
    for _, row in df.iterrows():
        region = row["Region"]
        epsg_code = row["EPSG"]
        epsg_options[f"{region}: {epsg_code}"] = epsg_code
    
    return epsg_options