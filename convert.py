import pandas as pd
import xml.etree.ElementTree as ET

def convert_excel_to_xml(excel_file, output_file):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_file)
    
    # Create the root element
    root = ET.Element("root")
    
    # Iterate over the rows in the DataFrame
    for _, row in df.iterrows():
        # Create a new record element
        record = ET.SubElement(root, "record")
        
        # Add sub-elements based on DataFrame columns
        for col in df.columns:
            child = ET.SubElement(record, col)
            child.text = str(row[col])
    
    # Convert the ElementTree to a string
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
