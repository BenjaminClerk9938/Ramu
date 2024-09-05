import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QLabel)
from PyQt5.QtCore import Qt
from convert import convert_excel_to_xml
from lxml import etree

class ExcelToXMLApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Excel to XML Converter')
        self.setGeometry(100, 100, 400, 200)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Excel file selection
        self.select_button = QPushButton('Select Excel File', self)
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)
        
        # XSD file selection
        self.select_xsd_button = QPushButton('Select XSD File (Optional)', self)
        self.select_xsd_button.clicked.connect(self.select_xsd_file)
        layout.addWidget(self.select_xsd_button)
        
        # Convert button
        self.convert_button = QPushButton('Convert to XML', self)
        self.convert_button.clicked.connect(self.convert_file)
        self.convert_button.setEnabled(False)
        layout.addWidget(self.convert_button)

        # Status label
        self.status_label = QLabel("", self)
        layout.addWidget(self.status_label)
        
        self.file_path = None
        self.xsd_path = None

    def select_file(self):
        options = QFileDialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        
        if self.file_path:
            self.convert_button.setEnabled(True)
            self.status_label.setText(f"Selected file: {os.path.basename(self.file_path)}")
        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid Excel file.")

    def select_xsd_file(self):
        options = QFileDialog.Options()
        self.xsd_path, _ = QFileDialog.getOpenFileName(self, "Select XSD File", "", "XSD Files (*.xsd);;All Files (*)", options=options)
        
        if self.xsd_path:
            self.status_label.setText(f"Selected XSD file: {os.path.basename(self.xsd_path)}")
        else:
            QMessageBox.warning(self, "No XSD File Selected", "XSD file not selected. XML validation will be skipped.")

    def convert_file(self):
        if self.file_path:
            output_file = os.path.join("output", "output.xml")
            try:
                # Ensure the output directory exists
                if not os.path.exists("output"):
                    os.makedirs("output")

                convert_excel_to_xml(self.file_path, output_file)

                if self.xsd_path:
                    if self.validate_xml(output_file, self.xsd_path):
                        QMessageBox.information(self, "Success", f"File successfully converted and validated. Saved as {output_file}")
                    else:
                        QMessageBox.warning(self, "Validation Error", "The XML file did not validate against the XSD schema.")
                else:
                    QMessageBox.information(self, "Success", f"File successfully converted and saved as {output_file}")
                
            except FileNotFoundError:
                QMessageBox.critical(self, "File Not Found", "The specified file was not found.")
            except PermissionError:
                QMessageBox.critical(self, "Permission Denied", "Permission denied to access or write the file.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def validate_xml(self, xml_file, xsd_file):
        try:
            # Load XSD schema
            with open(xsd_file, 'r') as xsd_f:
                xsd_root = etree.XML(xsd_f.read())
                schema = etree.XMLSchema(xsd_root)

            # Parse XML file
            with open(xml_file, 'r') as xml_f:
                xml_root = etree.XML(xml_f.read())

            # Validate XML against XSD
            schema.assertValid(xml_root)
            return True
        except etree.DocumentInvalid:
            return False
        except Exception as e:
            QMessageBox.critical(self, "Validation Error", f"An error occurred during validation: {e}")
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExcelToXMLApp()
    ex.show()
    sys.exit(app.exec_())
