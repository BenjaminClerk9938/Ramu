import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QMessageBox,
)
from convert import load_excel_data, create_xml_from_dataframe, save_xml, validate_xml
import os
from lxml import etree


class ExcelToXMLConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.initUI()

        # File paths
        self.excel_path = ""
        self.schema_path = ""
        self.output_path = "output/output.xml"

    def initUI(self):
        self.setWindowTitle("Excel to XML Converter")
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # Buttons
        self.select_excel_button = QPushButton("Select Excel File", self)
        self.select_excel_button.clicked.connect(self.select_excel_file)
        layout.addWidget(self.select_excel_button)

        self.select_schema_button = QPushButton("Select Schema File", self)
        self.select_schema_button.clicked.connect(self.select_schema_file)
        layout.addWidget(self.select_schema_button)

        self.convert_button = QPushButton("Convert to XML", self)
        self.convert_button.clicked.connect(self.convert_to_xml)
        layout.addWidget(self.convert_button)

        # Label
        self.status_label = QLabel("", self)
        layout.addWidget(self.status_label)

        # Set layout
        self.setLayout(layout)

    def select_excel_file(self):
        options = QFileDialog.Options()
        self.excel_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel File", "", "Excel Files (*.xlsx;*.xls)", options=options
        )
        if self.excel_path:
            self.status_label.setText(f"Excel File Selected: {self.excel_path}")

    def select_schema_file(self):
        options = QFileDialog.Options()
        self.schema_path, _ = QFileDialog.getOpenFileName(
            self, "Select Schema File", "", "XML Schema Files (*.xsd)", options=options
        )
        if self.schema_path:
            self.status_label.setText(f"Schema File Selected: {self.schema_path}")

    def convert_to_xml(self):
        if not self.excel_path or not self.schema_path:
            QMessageBox.warning(
                self, "Error", "Please select both Excel and Schema files."
            )
            return

        try:
            # Load Excel data
            df = load_excel_data(self.excel_path)

            # Create XML from DataFrame
            root = create_xml_from_dataframe(df)
            tree = etree.ElementTree(root)

            # Save XML to file
            save_xml(tree, self.output_path)

            # Validate XML against XSD
            if validate_xml(self.output_path, self.schema_path):
                QMessageBox.information(
                    self, "Success", "XML file generated and validated successfully!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "The XML file did not validate against the schema.",
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


def main():
    app = QApplication(sys.argv)
    ex = ExcelToXMLConverterApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
