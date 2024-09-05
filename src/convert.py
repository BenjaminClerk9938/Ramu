import pandas as pd
from lxml import etree

def load_excel_data(file_path):
    """Load Excel data into a pandas DataFrame."""
    return pd.read_excel(file_path)

def create_xml_from_dataframe(df):
    """Convert DataFrame to XML structure dynamically based on columns."""
    root = etree.Element('Records')
    
    for _, row in df.iterrows():
        record = etree.SubElement(root, 'Record')
        
        for column in df.columns:
            element = etree.SubElement(record, column)
            element.text = str(row[column])
    
    return root

def save_xml(tree, file_path):
    """Save the XML tree to a file."""
    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def validate_xml(xml_file, xsd_file):
    """Validate XML file against the schema."""
    xmlschema_doc = etree.parse(xsd_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    xml_doc = etree.parse(xml_file)
    
    return xmlschema.validate(xml_doc)
